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
RELEASE_FILES = ("lib.typ", "typst.toml", "README.md", "LICENSE", "NOTICE", "thumbnail.png")


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


def compile_pdf(source, output, *, root=ROOT, packages=None, stage="final"):
    output.parent.mkdir(parents=True, exist_ok=True)
    args = ["typst", "compile", "--root", root, "--ignore-system-fonts",
            "--creation-timestamp", os.environ.get("SOURCE_DATE_EPOCH", "0"),
            "--input", f"stage={stage}"]
    if packages:
        args += ["--package-path", packages, "--package-cache-path", packages / "cache"]
    run([*args, source, output])


def build(stage="final"):
    compile_pdf(ROOT / "main.typ", BUILD / ("fydp.pdf" if stage == "final" else "fydp-1.pdf"), stage=stage)


def copy_package(destination, *, thumbnail=True):
    destination.mkdir(parents=True, exist_ok=True)
    for name in RELEASE_FILES:
        if name == "thumbnail.png" and not thumbnail:
            continue
        shutil.copy2(ROOT / name, destination / name)
    for name in ("template", "docs"):
        shutil.copytree(ROOT / name, destination / name)


def initialized_project(scratch, *, thumbnail=True):
    packages = scratch / "packages"
    package = packages / "preview" / PACKAGE["name"] / PACKAGE["version"]
    copy_package(package, thumbnail=thumbnail)
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
    print(f"Submission directory: {destination}\nArchive: {archive}\nNothing has been uploaded.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("doctor", "build", "watch", "check", "thumbnail", "package"))
    parser.add_argument("--stage", choices=("final", "fydp-1"), default="final")
    args = parser.parse_args()
    doctor()
    if args.command == "doctor":
        return
    if args.command == "build":
        build(args.stage)
    elif args.command == "watch":
        BUILD.mkdir(exist_ok=True)
        output = "fydp.pdf" if args.stage == "final" else "fydp-1.pdf"
        run(["typst", "watch", "--root", ROOT, "--ignore-system-fonts", "--input", f"stage={args.stage}", ROOT / "main.typ", BUILD / output])
    elif args.command == "check":
        check()
    elif args.command == "thumbnail":
        make_thumbnail()
    elif args.command == "package":
        package()


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, subprocess.CalledProcessError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
