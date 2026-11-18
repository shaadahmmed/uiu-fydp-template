# Student guide

## Start a report

The easiest option is to open [the template on Typst Universe](https://typst.app/universe/package/academic-uiu-fydp/)
and click **Create project in app**. For local writing, follow the
[README's local setup](../README.md#prefer-working-on-your-computer).
Use a separate project for each report and back up your sources and assets.

Paths below refer to a project created in the web app or with `typst init`.
If you cloned the development repository instead, these files are under
`template/`; compile root `main.typ` and use the repository helper commands.

Edit `project.typ` first. Each student is a dictionary with `name` and
`id`; keep IDs in quotes to preserve leading zeros. Arrays with one item require
a trailing comma:

```typst
students: (
  (name: "Your Name", id: "011234567"),
  (name: "Teammate Name", id: "011234568"),
),
date: [November 2026],
supervisors: ([Supervisor Name, Assistant Professor],),
```

These fields go inside the existing `project` dictionary. Use an explicit date
instead of today's date so that later rebuilds keep the original submission date.

## Write chapters

Edit the corresponding file in `chapters/`. Every chapter should start
with one or two sentences describing its scope. Replace instructional paragraphs
with your own work and fill empty sections only where relevant.

| LaTeX                     | Typst                           |
| ------------------------- | ------------------------------- |
| `\chapter{Introduction}`  | `= Introduction`                |
| `\section{Objectives}`    | `== Objectives`                 |
| `\subsection{Scope}`      | `=== Scope`                     |
| `\textbf{bold}`           | `*bold*`                        |
| `\textit{italic}`         | `_italic_`                      |
| `\cite{key}`              | `@key`                          |
| `\label{fig:design}`      | `<fig:design>` after the figure |
| `Figure~\ref{fig:design}` | `@fig:design`                   |

Typst automatically supplies “Figure”, “Table”, “Chapter”, or “Equation” when
referencing a numbered element. Do not write `Figure @fig:design`.

Use `-` for bullets and `+` for numbered list items. A blank line starts a new
paragraph. Use `$ ... $` for mathematics and fenced code blocks for code listings.
The [Typst tutorial](https://typst.app/docs/tutorial/) covers the full syntax.

## Figures, tables, and citations

The project design chapter includes a working figure, equation, and references.
Figure paths are relative to the file containing the image call. From a chapter:

```typst
#figure(
  image("../assets/context.svg", width: 100%, alt: "Describe the diagram."),
  caption: [System context.],
) <fig:system>

The system boundary is shown in @fig:system.
```

Wrap tables in `figure(..., kind: table, caption: [...])` so they appear in the
List of Tables. The standards chapter provides two examples. Replace dashes with
your actual assessment and explain every selected mapping. Do not copy example
mapping claims without evidence.

Add BibTeX entries to `references.bib` and cite them using `@key`. Typst
builds the IEEE numeric bibliography in citation order; no BibTeX command or
repeated compile passes are needed. The inherited algorithm-design book is a
syntax example; remove it and its citation if it is irrelevant to your work.

## FYDP-1 and final reports

In `content.typ`, change `default: "final"` to `default: "fydp-1"` for FYDP-1.
Leave it as `"final"` for the final report. This works in the web app and local
editor previews.

For a local initialized project, you can also select the stage when compiling:

```sh
typst compile --input stage=fydp-1 main.typ fydp-1.pdf
typst compile --input stage=final main.typ report.pdf
```

The CLI argument takes priority over the default. If you cloned the development
repository, use `python3 scripts/project.py build --stage fydp-1` or
`python3 scripts/project.py build --stage final` instead; those outputs are
`build/fydp-1.pdf` and `build/fydp.pdf`.

FYDP-1 omits implementation and results. You may include a preliminary version by
editing that conditional include, with your educator's guidance. Introduction,
background, project design, standards and constraints, and conclusion are in both
versions. Renumbering is automatic.

## Front matter and logo

Abstract and acknowledgements are enabled by default. Edit their files in
`front-matter/`. Uncomment the `publications` entry in `project.typ` to
enable that page, and include only actual publications with accurate status.
Use `abstract: none` or `acknowledgements: none` to omit a page if permitted.

Reports do not require a logo. To add an approved logo to a web or locally
initialized project, place it in `assets/` and replace the existing show rule in
`main.typ` with:

```typst
#show: fydp-report.with(..project, logo: image("assets/my-logo.png", width: 28mm))
```

Do not add a second `logo` argument if one is already present in your dictionary.

For development repository checkouts, put an approved logo in `local-assets/` and
run `python3 scripts/project.py build --logo local-assets/uiu.png`. That directory
is ignored by Git and omitted from the package.

## Before submission

- Replace all example names, IDs, dates, diagrams, prose, and table dashes.
- Check that every citation is real and every claim is supported.
- Verify stage-specific requirements with your supervisor.
- Review the contents, Roman/Arabic numbering, captions, engineering mappings,
  bibliography, and all page breaks in the exported PDF.
- Retain the template attribution when distributing adapted material. Your
  project content remains your own work.

## Troubleshooting

| Problem                          | Fix                                                                                                                                                 |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Package download fails           | Check your internet connection and that the import uses `@preview/academic-uiu-fydp:0.1.0`. Local initialization needs network access on first use. |
| File outside project root        | Keep chapters and assets inside your project folder. For a repository checkout, compile root `main.typ` with `--root .`.                            |
| Missing image                    | Check the path relative to the chapter file, including capitalization.                                                                              |
| Unknown citation or reference    | Check the BibTeX key or `<label>` spelling.                                                                                                         |
| Font differs between machines    | Use the same compiler version and, locally, compile with `--ignore-system-fonts`.                                                                   |
| Changes do not appear in the PDF | Check that `main.typ` is the entry point. Export a fresh PDF in the web app, or rebuild and open your chosen local output file.                     |
| Empty List of Figures/Tables     | Add captioned figures or set the relevant `show-…-list` option to `false`.                                                                          |
| Typst syntax error               | Check commas in dictionaries, matching brackets, and the first compiler diagnostic.                                                                 |
