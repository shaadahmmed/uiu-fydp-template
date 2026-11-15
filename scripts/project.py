#!/usr/bin/env python3
"""Dependency-free build and release helpers. Requires Python 3.11+ and Typst."""

import argparse
import hashlib
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import tarfile
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
DIST = ROOT / "dist"
MANIFEST = tomllib.loads((ROOT / "typst.toml").read_text())
PACKAGE = MANIFEST["package"]
SPEC = f'@preview/{PACKAGE["name"]}:{PACKAGE["version"]}'
RELEASE_FILES = ("lib.typ", "typst.toml", "LICENSE", "NOTICE", "CHANGELOG.md", "thumbnail.png")


def run(args, *, cwd=ROOT, capture=False):
    print("+", " ".join(map(str, args)), flush=True)
    return subprocess.run(
        list(map(str, args)), cwd=cwd, check=True, text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def doctor():
    if not shutil.which("typst"):
        raise RuntimeError("Typst is missing. Install the latest stable version; see README.md.")
    actual = run(["typst", "--version"], capture=True).stdout.strip()
    match = re.search(r"typst (\d+)\.(\d+)\.(\d+)", actual)
    if not match or tuple(map(int, match.groups())) < tuple(map(int, PACKAGE["compiler"].split("."))):
        raise RuntimeError(f'Typst >= {PACKAGE["compiler"]} required; found {actual}.')
    pinned = (ROOT / ".typst-version").read_text().strip()
    if actual.split()[1] != pinned:
        print(f"Note: {actual}; reproducible builds use {pinned}.")
    print(f"Ready: {actual}; Python {sys.version.split()[0]}; no external Typst packages or fonts needed.")


def compile_pdf(source, output, *, root=ROOT, packages=None, stage="final", logo=None):
    output.parent.mkdir(parents=True, exist_ok=True)
    args = ["typst", "compile", "--root", root, "--ignore-system-fonts",
            "--creation-timestamp", os.environ.get("SOURCE_DATE_EPOCH", "0"),
            "--input", f"stage={stage}"]
    if packages:
        args += ["--package-path", packages, "--package-cache-path", packages / "cache"]
    if logo:
        args += ["--input", f"logo={logo}"]
    run([*args, source, output])


def build(stage="final", logo=None):
    compile_pdf(ROOT / "main.typ", BUILD / ("fydp.pdf" if stage == "final" else "fydp-1.pdf"), stage=stage, logo=logo)


def copy_package(destination, *, thumbnail=True):
    destination.mkdir(parents=True, exist_ok=True)
    for name in RELEASE_FILES:
        if name == "thumbnail.png" and not thumbnail:
            continue
        shutil.copy2(ROOT / name, destination / name)
    # Universe readers receive package instructions, not repository-only commands.
    shutil.copy2(ROOT / "packaging/README.md", destination / "README.md")
    for name in ("template", "docs"):
        shutil.copytree(ROOT / name, destination / name)


def validate_package_files(package):
    """Check documentation as shipped, with paths relative to the staged package."""
    for document in (package / "README.md", *(package / "docs").glob("*.md")):
        for target in re.findall(r"\]\(([^)]+)\)", document.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            if not (document.parent / target.split("#")[0]).exists():
                raise RuntimeError(f"Broken package documentation link in {document.name}: {target}")
    if (package / "uiu.png").exists() or (package / "local-assets").exists():
        raise RuntimeError("Local logos must not be distributed in the package.")


def initialized_project(scratch, *, thumbnail=True):
    packages = scratch / "packages"
    package = packages / "preview" / PACKAGE["name"] / PACKAGE["version"]
    copy_package(package, thumbnail=thumbnail)
    validate_package_files(package)
    project = scratch / "student-project"
    run(["typst", "init", "--package-path", packages, "--package-cache-path", packages / "cache", SPEC, project])
    return packages, project


def make_thumbnail():
    with tempfile.TemporaryDirectory(prefix=f'{PACKAGE["name"]}-thumbnail-') as directory:
        packages, project = initialized_project(Path(directory), thumbnail=False)
        run(["typst", "compile", "--root", project, "--ignore-system-fonts",
             "--package-path", packages, "--package-cache-path", packages / "cache",
             "--pages", "1", "--ppi", "150", project / "main.typ", ROOT / "thumbnail.png"])


def validate_metadata():
    expected = f'#import "{SPEC}": fydp-report, guidance'
    if expected not in (ROOT / "template/main.typ").read_text():
        raise RuntimeError("Template package import does not match manifest name/version.")
    if PACKAGE["compiler"] != (ROOT / ".typst-version").read_text().strip():
        raise RuntimeError("Update compiler and .typst-version together.")
    if not PACKAGE.get("repository", "").startswith("https://github.com/"):
        raise RuntimeError("Set a public source repository URL in typst.toml.")
    if f'## {PACKAGE["version"]} ' not in (ROOT / "CHANGELOG.md").read_text():
        raise RuntimeError("Add a changelog entry for the package version.")
    # Catch stale imports when preparing a new version.
    for document in (ROOT / "README.md", ROOT / "packaging/README.md", *(ROOT / "docs").glob("*.md")):
        imports = re.findall(rf'@preview/{re.escape(PACKAGE["name"])}:([0-9]+\.[0-9]+\.[0-9]+)', document.read_text())
        if any(version != PACKAGE["version"] for version in imports):
            raise RuntimeError(f"Stale package version in {document.relative_to(ROOT)}.")
    if PACKAGE["license"] != "CC-BY-4.0" or "Attribution 4.0 International" not in (ROOT / "LICENSE").read_text():
        raise RuntimeError("Manifest and license must agree.")
    data = (ROOT / "thumbnail.png").read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or len(data) > 3 * 1024 * 1024:
        raise RuntimeError("Thumbnail must be a PNG of at most 3 MiB.")
    width, height = struct.unpack(">II", data[16:24])
    if max(width, height) < 1080:
        raise RuntimeError("Thumbnail's longer edge must be at least 1080 pixels.")


def check():
    validate_metadata()
    build()
    build("fydp-1")
    with tempfile.TemporaryDirectory(prefix=f'{PACKAGE["name"]}-check-') as directory:
        scratch = Path(directory)
        packages, project = initialized_project(scratch)
        # A real init, in a new root, catches hidden dependencies on this repository.
        compile_pdf(project / "main.typ", BUILD / "package-final.pdf", root=project, packages=packages)
        compile_pdf(project / "main.typ", BUILD / "package-fydp-1.pdf", root=project, packages=packages, stage="fydp-1")
        # Exercise optional front matter and multiple authors, then the minimal API.
        (project / "options.typ").write_text(
            f'#import "{SPEC}": fydp-report\n'
            '#show: fydp-report.with(\n'
            ' title: [A Longer Project Title for a Configurable Final Year Design Report],\n'
            ' students: ((name: "First Student", id: "1"), (name: "Second Student", id: "2"),\n'
            ' (name: "Third Student", id: "3")),\n'
            ' supervisors: ([First Supervisor], [Second Supervisor]),\n'
            ' abstract: [Abstract text.], acknowledgements: [Acknowledgements text.],\n'
            ' publications: include "front-matter/publications.typ",\n'
            ' show-figure-list: false, show-table-list: false,\n'
            ')\n= Sample Chapter\nSample body.\n'
        )
        compile_pdf(project / "options.typ", BUILD / "options.pdf", root=project, packages=packages)
        (project / "minimal.typ").write_text(
            f'#import "{SPEC}": fydp-report\n'
            '#show: fydp-report.with(show-figure-list: false, show-table-list: false)\n'
            '= Minimal Chapter\nMinimal body.\n'
        )
        compile_pdf(project / "minimal.typ", BUILD / "minimal.pdf", root=project, packages=packages)
        readme = (packages / "preview" / PACKAGE["name"] / PACKAGE["version"] / "README.md").read_text()
        for index, example in enumerate(re.findall(r"```typst\n(.*?)```", readme, re.DOTALL), start=1):
            source = project / f"readme-example-{index}.typ"
            source.write_text(example)
            compile_pdf(source, BUILD / f"readme-example-{index}.pdf", root=project, packages=packages)
    print("Checks passed: local reports, initialized package, FYDP-1, optional pages, minimal API, and metadata.")


def package():
    # Rebuild the thumbnail and verify the exact files that will be distributed.
    make_thumbnail()
    check()
    DIST.mkdir(exist_ok=True)
    destination = DIST / PACKAGE["name"] / PACKAGE["version"]
    if destination.exists():
        shutil.rmtree(destination)
    copy_package(destination)
    archive = DIST / f'{PACKAGE["name"]}-{PACKAGE["version"]}.tar.gz'
    with tarfile.open(archive, "w:gz") as bundle:
        bundle.add(destination, arcname=f'{PACKAGE["name"]}/{PACKAGE["version"]}')
    checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix(archive.suffix + ".sha256").write_text(f"{checksum}  {archive.name}\n")
    pr_description = f'''Adds {PACKAGE["name"]} {PACKAGE["version"]} for United International University
CSE final year design project reports.

- Source: {PACKAGE["repository"]}
- Typst adaptation: Shaad Ahmmed (@shaadahmmed).
- Original LaTeX template: Swakkhar Shatabda, available on Overleaf under CC BY 4.0:
  https://www.overleaf.com/latex/templates/united-international-university-fydp-template-department-of-cse/xbkpdgkgjdhc
- License: CC-BY-4.0; the package includes LICENSE, NOTICE, and a changes notice.
- Community adaptation; no claim of university endorsement. No university logo is bundled.
- Includes FYDP-1/final variants, editable chapters, configurable front matter,
  engineering mapping tables, and student/educator documentation.
- Validation: local and freshly initialized package reports in both stages,
  optional front matter and multiple students, minimal API, package documentation
  links, manifest/version consistency, and thumbnail dimensions.
- Tested locally with {run(["typst", "--version"], capture=True).stdout.strip()}.

Use the current upstream PR template and add this description. Confirm any upstream
checkboxes yourself; this generated text does not claim that review or publication
has already happened.
'''
    (DIST / "universe-pr.md").write_text(pr_description)
    print(f"Submission directory: {destination}\nArchive: {archive}\nNothing has been uploaded.")


def stage_submission(packages_repo):
    """Copy into an existing packages clone; never overwrite an existing release."""
    packages_repo = packages_repo.resolve()
    if packages_repo == ROOT or not (packages_repo / ".git").exists() or not (packages_repo / "packages/preview").is_dir():
        raise RuntimeError("--packages-repo must point to a clone of your typst/packages fork with packages/preview checked out.")
    destination = packages_repo / "packages/preview" / PACKAGE["name"] / PACKAGE["version"]
    if not destination.resolve().is_relative_to(packages_repo):
        raise RuntimeError("The submission path must stay inside the packages clone.")
    if destination.exists():
        raise RuntimeError(f"Refusing to overwrite an existing version: {destination}. Review it or use a new version.")
    package()
    shutil.copytree(DIST / PACKAGE["name"] / PACKAGE["version"], destination)
    print(f"Staged: {destination}\nReview and commit this directory in your fork, then open a PR to typst/packages.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("doctor", "build", "watch", "check", "thumbnail", "package", "stage"))
    parser.add_argument("--stage", choices=("final", "fydp-1"), default="final")
    parser.add_argument("--logo", help="Optional logo path relative to the repository, for local build/watch only.")
    parser.add_argument("--packages-repo", type=Path, help="Path to your typst/packages fork clone (required for stage).")
    args = parser.parse_args()
    if args.command == "stage" and args.packages_repo is None:
        parser.error("stage requires --packages-repo PATH")
    if args.logo and args.command not in ("build", "watch"):
        parser.error("--logo is supported by build and watch only")
    doctor()
    if args.command == "doctor":
        return
    if args.command == "build":
        build(args.stage, args.logo)
    elif args.command == "watch":
        BUILD.mkdir(exist_ok=True)
        output = "fydp.pdf" if args.stage == "final" else "fydp-1.pdf"
        logo_input = ["--input", f"logo={args.logo}"] if args.logo else []
        run(["typst", "watch", "--root", ROOT, "--ignore-system-fonts", "--input", f"stage={args.stage}", *logo_input, ROOT / "main.typ", BUILD / output])
    elif args.command == "check":
        check()
    elif args.command == "thumbnail":
        make_thumbnail()
    elif args.command == "package":
        package()
    elif args.command == "stage":
        stage_submission(args.packages_repo)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, subprocess.CalledProcessError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
