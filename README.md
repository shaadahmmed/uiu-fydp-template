# UIU CSE Final Year Design Project Report (Typst)

A community Typst adaptation of the **United International University Final Year
Design Project template, Department of Computer Science and Engineering**.
Converted by **Shaad Ahmmed** from the LaTeX template by **Swakkhar Shatabda**.

Use this starter for FYDP-1 and final reports. It includes a title page, abstract,
acknowledgements, optional publications, contents, figure and table lists, six
chapters, engineering mapping tables, and a numeric bibliography. A4 pages, 3 cm
margins, 11 pt New Computer Modern, chapter page breaks, running chapter headers,
Roman preliminary page numbers, and Arabic body page numbers follow the supplied
LaTeX structure. Line spacing approximates LaTeX's one-and-a-half spacing.

**Status:** version 0.1.0 is prepared for submission; it is **not yet published on
Typst Universe**. Use the local instructions below now. This is a community
adaptation; confirm current submission requirements with your supervisor.

## Start here

| Your goal | Where to go |
| --- | --- |
| Write your report | [Student guide](docs/STUDENTS.md) |
| Teach or distribute the template | [Educator guide](docs/EDUCATORS.md) |
| Configure the report | [Configuration reference](docs/CONFIGURATION.md) |
| Publish or update the package | [Publishing guide](docs/PUBLISHING.md) |
| Understand the conversion | [LaTeX migration notes](docs/MIGRATION.md) |
| Review version changes | [Changelog](CHANGELOG.md) |

## Local environment

These instructions use the full development checkout. A project initialized
from the published template only needs Typst and its own `main.typ`.

1. Install the **latest stable version of Typst** from the
   [official latest release](https://github.com/typst/typst/releases/latest).
   Extract the archive for your operating system and place the `typst` executable
   on your `PATH`. Alternatively, use one of the installation commands below.
2. Install **Python 3.11 or newer** for the optional build/release helpers.
   Python's standard library is sufficient; no `pip` packages or virtual
   environment are needed. GNU Make is optional.
3. Open a terminal in this directory, then run:

   ```sh
   typst --version
   python3 scripts/project.py doctor
   python3 scripts/project.py build
   ```

| Platform or tool | Install command |
| --- | --- |
| macOS (Homebrew) | `brew install typst` |
| Windows (WinGet) | `winget install --id Typst.Typst` |
| Any platform with a compatible Rust toolchain | `cargo install --locked typst-cli` |
| Linux or manual installation | Download the archive for your platform from the [latest release](https://github.com/typst/typst/releases/latest). |

Package-manager versions can lag behind the latest release. For a manually
installed official binary, run `typst update` to update it; for package-manager
installations, use that package manager's upgrade command. See the
[official installation instructions](https://github.com/typst/typst#installation).

The template requires **Typst 0.15.0 or newer**. Use the latest stable release for
normal writing. [.typst-version](.typst-version) and CI record **0.15.0** as the
tested baseline for reproducible builds; newer stable versions are accepted by
the build helper.

On Windows, use `py -3` in place of `python3` if needed. Generated reports go to
`build/`; the default output is **`build/fydp.pdf`**.

Typst embeds the fonts used here. The build helper ignores system fonts for
consistent output and does not download Typst packages. No LaTeX installation is
required. The compiler is already available in the original development workspace.

You can also compile without Python:

```sh
mkdir -p build
typst compile --root . --ignore-system-fonts main.typ build/fydp.pdf
typst watch --root . --ignore-system-fonts main.typ build/fydp.pdf
```

Create `build` using File Explorer or `mkdir build` on Windows. VS Code users can
install the recommended **Tinymist** extension, open the repository directory,
and preview **root `main.typ`**. The checked-in settings use the workspace as the
project root and leave PDF export to the build command.

## Write your report

1. Edit **`template/project.typ`**: title, student names and IDs, explicit date,
   supervisors, and front-matter options.
2. Replace the text in **`template/front-matter/`** and **`template/chapters/`**.
3. Replace the example diagram in `template/assets/` and update
   **`template/references.bib`** with sources you actually use.
4. Build and review the PDF, including its contents, lists, citations, and tables.

```sh
python3 scripts/project.py watch
python3 scripts/project.py build --stage fydp-1
```

FYDP-1 omits the implementation chapter by default. Both stages retain the
introduction, background, design, standards and constraints, and conclusion.
Set the default stage in `template/content.typ` if you use an editor or web app;
the CLI input `--input stage=fydp-1` overrides that default.

Reports build without a logo by default. For a local logo, place your approved
image in the ignored `local-assets/` directory and run:

```sh
python3 scripts/project.py build --logo local-assets/uiu.png
```

The original workspace logo, if present, is kept there for local use. Local
assets are excluded from Git and the Universe bundle. A project initialized from
the package can supply its own image through the `logo` parameter.

## Typst web app

Until Universe publication, create a blank project at [typst.app](https://typst.app/)
and upload **root `main.typ`, `lib.typ`, and the entire `template/` directory**
from your local copy. Keep the directory structure and set root `main.typ` as
the main file. Upload `NOTICE` and `LICENSE` alongside the sources. Use the latest
stable compiler, version 0.15.0 or newer. No logo upload is required.

The `template/main.typ` entry point is for initialized package projects. It uses
an `@preview` import and will not resolve online until the package is accepted.

## Package usage after publication

These commands are for **after acceptance on Typst Universe**:

```sh
typst init @preview/academic-uiu-fydp:0.1.0 my-fydp
cd my-fydp
typst compile main.typ report.pdf
```

The generated project owns its chapter files and configuration. Styling stays in
the versioned package. A minimal report would be:

```typst
#import "@preview/academic-uiu-fydp:0.1.0": fydp-report
#show: fydp-report.with(
  title: [My Final Year Design Project],
  students: ((name: "Student Name", id: "011 XXX XXX"),),
  date: [November 2026],
  show-figure-list: false,
  show-table-list: false,
)

= Introduction
Introduce your project here.
```

For the same example in a repository checkout, replace the import path with
`"lib.typ"` and save it at the root.

## Build and release commands

| Task | Portable command | Make alias |
| --- | --- | --- |
| Check environment | `python3 scripts/project.py doctor` | `make setup` |
| Final report | `python3 scripts/project.py build` | `make build` |
| FYDP-1 report | `python3 scripts/project.py build --stage fydp-1` | `make fydp-1` |
| Live preview | `python3 scripts/project.py watch` | `make watch` |
| Compile integration checks | `python3 scripts/project.py check` | `make check` |
| Refresh the logo-free thumbnail | `python3 scripts/project.py thumbnail` | `make thumbnail` |
| Validate and prepare distribution | `python3 scripts/project.py package` | `make package` |
| Stage into your Universe fork | `python3 scripts/project.py stage --packages-repo ../typst-packages` | — |

Checks initialize the package in a temporary, isolated package directory, then
compile the generated starter in both stages and exercise optional front matter,
multiple students, and the minimal API. The release command produces
`dist/academic-uiu-fydp/0.1.0/`, a `.tar.gz` archive, and its SHA-256 checksum. It uploads
nothing. It also writes a draft submission description to `dist/universe-pr.md`.
The bundle uses [a package-specific README](packaging/README.md) so Universe
readers get instructions that match the distributed files.

CI performs the packaging checks with both the tested baseline and the latest
stable Typst release and retains report PDFs and the release archive as artifacts.
To publish, follow [the repository-specific publishing steps](docs/PUBLISHING.md).
Updating this GitHub repository or passing CI does not publish to Universe.

## Files

```text
main.typ                    Local report entry point; optional user-supplied logo
lib.typ                     Reusable report layout and styling
typst.toml                  Package and template metadata
template/
  main.typ                  Package starter entry point
  project.typ               Student and report metadata
  content.typ               Chapter selection and bibliography
  front-matter/             Abstract, acknowledgements, optional publications
  chapters/                 Six editable report chapters
  assets/context.svg        Replaceable example diagram
  references.bib            BibTeX bibliography
  NOTICE.md                 Attribution copied into initialized projects
docs/                       Student, educator, configuration, publishing guides
scripts/project.py          Portable build and packaging helper
packaging/README.md         README used in the Universe submission bundle
CHANGELOG.md                Version history
local-assets/               Optional local images; ignored and not distributed
```

## License and attribution

The original [Overleaf template](https://www.overleaf.com/latex/templates/united-international-university-fydp-template-department-of-cse/xbkpdgkgjdhc)
is credited to **Swakkhar Shatabda** and listed under **Creative Commons
Attribution 4.0 International (CC BY 4.0)**. This adaptation by **Shaad Ahmmed**
uses the same license. See [LICENSE](LICENSE), [NOTICE](NOTICE), and the
[license terms](https://creativecommons.org/licenses/by/4.0/).

When sharing adapted template material, retain appropriate credit, a license
link, and an indication of your changes. The starter includes an acknowledgement
you can use. The license on this template does not automatically license your
original research, prose, results, or data.

No university logo is distributed in the public source or Universe bundle.
The original workspace logo, if present, is kept in ignored `local-assets/`;
no separate redistribution clearance for it has been established.
University names and trademarks are not licensed by this project. The included
example context diagram was created for this adaptation and uses the template's
CC BY 4.0 license.
