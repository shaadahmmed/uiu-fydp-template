# From Overleaf to Typst

**Already writing your FYDP report on Overleaf? Keep your content; let this
template handle the layout.** You do not need to rewrite your research or learn
all of Typst before starting.

> Check with your supervisor first. If submission requires `.tex` source or a
> particular LaTeX class, stay with LaTeX. Typst produces a PDF, but its source
> files are not interchangeable with LaTeX and pagination will differ.

**The short version:** back up Overleaf → create a Typst project → move your
text, images, and references → convert one chapter at a time → review the PDF.

## 1. Save your Overleaf project

From your Overleaf project's menu, download:

- **The source ZIP:** your `.tex` files, `.bib` bibliography, images, and other assets.
- **The latest PDF:** keep it as a reference for checking that nothing was lost.

Extract the ZIP on your computer. Keep the original project unchanged until the
Typst report is complete. Comments, tracked changes, and project history do not
become Typst content through a source download; resolve or record important
feedback separately.

## 2. Create a fresh Typst report

1. Open [this template on Typst Universe](https://typst.app/universe/package/academic-uiu-fydp/).
2. Click **Create project in app** and sign in if prompted.
3. Edit **`project.typ`**: title, team members, IDs, date, and supervisors.
4. Keep **`main.typ`** as the entry point. Do not replace it with your old `.tex` file.

Prefer a local editor? Follow the [local setup](../README.md#prefer-working-on-your-computer)
instead. The file paths below apply to web and `typst init` projects. In a cloned
development repository, the editable files are inside `template/`.

## 3. Put your existing material in the right place

| From your Overleaf project                   | Put it in the Typst project      |
| -------------------------------------------- | -------------------------------- |
| Title, authors, IDs, date, supervisor        | `project.typ`                    |
| Abstract and acknowledgements                | Files in `front-matter/`         |
| Introduction                                 | `chapters/01-introduction.typ`   |
| Background and related work                  | `chapters/02-background.typ`     |
| Requirements, design, plan, task allocation  | `chapters/03-project-design.typ` |
| Implementation, tests, results               | `chapters/04-implementation.typ` |
| Standards, constraints, engineering mappings | `chapters/05-standards.typ`      |
| Conclusion and future work                   | `chapters/06-conclusion.typ`     |
| Images and diagrams                          | `assets/`                        |
| Entries from your `.bib` file                | `references.bib`                 |

**Move content, not the old formatting setup.** Leave behind
`\documentclass`, `\usepackage`, `\begin{document}`, `\end{document}`, title-page
code, page styles, and commands that generate the contents or bibliography.
The Typst template already supplies these. Do not upload `.aux`, `.log`, `.toc`,
`.bbl`, or other LaTeX build outputs.

Start with **one short chapter**, not the whole report. Replace its example text,
convert its syntax, and check the preview before moving to the next chapter.
Keep one chapter heading per chapter file; do not paste a second heading beneath
the starter's existing heading.

## 4. Translate the common syntax

### A small before-and-after example

**Overleaf / LaTeX:**

```latex
\chapter{Background}
\label{ch:background}

\section{Related Work}
We compare the \textbf{main approaches} to algorithm design
\cite{kleinberg2006algorithm}.
```

**Typst — paste into `chapters/02-background.typ`, replacing its sample content:**

```typst
= Background <ch:background>

== Related Work
We compare the *main approaches* to algorithm design
@kleinberg2006algorithm.
```

This citation uses the starter's example book. Use your own bibliography keys
and relevant sources in the actual report.

### Keep this cheat sheet nearby

| What you need       | LaTeX                      | Typst                                         |
| ------------------- | -------------------------- | --------------------------------------------- |
| Chapter             | `\chapter{Introduction}`   | `= Introduction`                              |
| Section             | `\section{Objectives}`     | `== Objectives`                               |
| Subsection          | `\subsection{Scope}`       | `=== Scope`                                   |
| Bold                | `\textbf{important}`       | `*important*`                                 |
| Italic              | `\textit{term}`            | `_term_`                                      |
| Bullet item         | `\item` inside `itemize`   | `- Item text` on its own line                 |
| Numbered item       | `\item` inside `enumerate` | `+ Item text` on its own line                 |
| New paragraph       | Blank line                 | Blank line                                    |
| Comment             | `% comment`                | `// comment`                                  |
| Citation            | `\cite{key}`               | `@key`                                        |
| Label               | `\label{ch:intro}`         | `<ch:intro>` after the heading                |
| Reference           | `\ref{ch:intro}`           | `@ch:intro`                                   |
| Include a chapter   | `\input{chapters/extra}`   | `#include "chapters/extra.typ"`               |
| Inline mathematics  | `$x^2$`                    | `$x^2$`                                       |
| Display mathematics | `\[ x^2 \]`                | `$ x^2 $` with spaces inside the dollar signs |

**Important differences:**

- Keep existing chapter labels such as `<ch:background>` when replacing starter
  text; other chapters may reference them. If you rename a label, update its
  references too, and avoid duplicate labels.
- Typst references supply the element name automatically. Write `See @fig:system`,
  not `See Figure @fig:system`, or you may get “Figure Figure …”.
- `%` is ordinary text in Typst, not a comment. Convert LaTeX comments to `//`.
- In normal Typst text, write `50%` and `A & B`, not `50\%` and `A \& B`.
  For literal `#`, `@`, or `$`, use `\#`, `\@`, or `\$`.
- Do not replace every backslash blindly. Equations, custom commands, and tables
  need attention to meaning, not just search-and-replace.

### Images and captions

Upload the original image to `assets/`. This example uses the diagram already
included in the starter; replace its filename, caption, and description with yours.
From a file in `chapters/`:

```typst
#figure(
  image("../assets/context.svg", width: 80%, alt: "Example system context diagram."),
  caption: [System context; replace with your project diagram.],
) <fig:migrated-context>

The system boundary is shown in @fig:migrated-context.
```

Paths are relative to the file containing `image(...)`, so a chapter uses
`../assets/`, not `assets/`. PNG, JPEG, and SVG are useful portable choices.
TikZ/PGF source does not run in Typst: export the diagram to a supported image
format or redraw it with Typst tools. For PDF figures, see the
[image format documentation](https://typst.app/docs/reference/visualize/image/)
for the supported PDF subset; convert unsupported files to SVG or PNG.

### Tables

Replace `tabular` environments with `table(...)`. Wrap the table in `figure` so
it receives a caption, a number, and an entry in the List of Tables:

```typst
#figure(
  table(
    columns: (1fr, 2fr),
    table.header([Requirement], [How it will be checked]),
    [Login], [Test valid and invalid credentials],
    [Search], [Compare results with the expected matches],
  ),
  kind: table,
  caption: [Example verification plan; adapt to your project.],
) <tab:migrated-plan>

Our verification plan is summarized in @tab:migrated-plan.
```

For the standards and engineering mapping tables, fill in the examples already
in `chapters/05-standards.typ`. Keep only claims supported by your own work.

### Equations

Simple formulas may look familiar, but Typst math is **not LaTeX math**:

| LaTeX                | Typst             |
| -------------------- | ----------------- |
| `\alpha`             | `alpha`           |
| `\frac{a}{b}`        | `a / b`           |
| `x_{i+1}`            | `x_(i+1)`         |
| `\sum_{i=1}^{n} x_i` | `sum_(i=1)^n x_i` |
| `\text{accuracy}`    | `"accuracy"`      |

For a numbered, referenceable equation:

```typst
#set math.equation(numbering: "(1)")
$ "accuracy" = "correct predictions" / "total predictions" $ <eq:migrated-accuracy>

We evaluate the model using @eq:migrated-accuracy.
```

Put multi-letter words in quotes; otherwise Typst may interpret them as variable
names. Check each equation visually against the original PDF. See the
[math guide for LaTeX users](https://typst.app/docs/guides/for-latex-users/#how-do-i-input-maths)
for more examples.

## 5. Reuse your bibliography and choose the report stage

- Copy your `.bib` entries into **`references.bib`**, or replace that file with
  your existing bibliography using the same filename. Preserve the entry keys.
- Change citations such as `\cite{your-key}` to `@your-key`. Remove the starter's
  book entry and citation if they are not relevant.
- Keep the **single** `#bibliography(...)` call already in `content.typ`. Do not
  paste `\bibliography`, `\bibliographystyle`, or a second bibliography into chapters.
- Typst uses the BibTeX data directly; you do not run BibTeX or Biber. Review
  titles containing LaTeX commands, special characters, and unsupported fields.
  Bibliography formatting is IEEE numeric here, not necessarily your old style.
- For **FYDP-1**, change `default: "final"` to `default: "fydp-1"` in `content.typ`.
  Leave `"final"` for the final report. The FYDP-1 setting omits implementation
  and results; confirm your supervisor's required sections.

## 6. Check before switching over completely

Compare the PDFs for **content completeness**, not identical page breaks:

- [ ] All chapters, abstract, acknowledgements, and required extra sections are present.
- [ ] All images, tables, equations, captions, and labels survived the move.
- [ ] Every citation resolves to the correct source; no sample citations remain.
- [ ] The contents and figure/table lists are correct, with no duplicate headings.
- [ ] Names, IDs, supervisor details, date, and report stage are correct.
- [ ] No LaTeX commands, old comments, or template instructions remain in the output.
- [ ] Important supervisor feedback has been addressed or recorded separately.
- [ ] Your supervisor accepts the exported PDF and any required source format.
- [ ] Both the original Overleaf backup and the new Typst sources are saved.

**Stuck?** Fix the first compiler error before the later ones. Check image paths,
missing bibliography keys, unmatched brackets, and leftover LaTeX commands.

### Can I convert automatically?

The Typst web app offers LaTeX import, which can help with basic content. Treat
its output as a **draft**, not a finished FYDP report: move the converted body
into this template's chapter files rather than replacing its entry point or
layout. Custom macros, package-specific environments, equations, references, and
figures still need review. For short reports, manual chapter-by-chapter migration
is often easier to check.

Continue with the [student guide](STUDENTS.md) for everyday writing, the
[configuration reference](CONFIGURATION.md) for report options, or the
[original conversion notes](MIGRATION.md) for layout differences from the LaTeX
template. The [official LaTeX-to-Typst guide](https://typst.app/docs/guides/for-latex-users/)
covers language differences in more detail.
