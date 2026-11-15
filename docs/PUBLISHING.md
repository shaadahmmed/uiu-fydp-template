# Publish UIU CSE Final Year Design Project Report

The package is prepared locally as **`academic-uiu-fydp` version `0.1.0`**. It has not
been submitted, accepted, or published. A public GitHub repository URL has not yet
been provided; add it to `typst.toml` when the repository exists.

The manifest credits Shaad Ahmmed as the Typst author and Swakkhar Shatabda for
the original LaTeX. Keep that distinction in your release and submission text.

## Prepare a public repository

1. Create a repository under your own account and upload this project. Keep
   `README.md`, `LICENSE`, and `NOTICE` visible. Review original assets before
   publishing them; the original logo's redistribution terms are not established.
2. Add the actual `repository = "https://github.com/OWNER/REPOSITORY"` field under
   `[package]` in `typst.toml`. Replace the example with your real URL.
3. Check that the proposed name is free in
   [Typst Universe](https://typst.app/universe/) and the
   [package repository](https://github.com/typst/packages/tree/main/packages/preview).
   A local build does not reserve a package name.
4. Review the current official [submission instructions](https://github.com/typst/packages/blob/main/docs/README.md),
   [manifest rules](https://github.com/typst/packages/blob/main/docs/manifest.md),
   and [licensing rules](https://github.com/typst/packages/blob/main/docs/licensing.md).

Before uploading the development checkout, remove or obtain clear redistribution
permission for the original logo and adjust root `main.typ` to compile without it
if removed. The curated `dist` directory is intended for the Universe
submission; it does not contain the development tools or local entry point.

## Build the submission

Run from the development repository:

```sh
python3 scripts/project.py package
```

This command refreshes the thumbnail from the **initialized, logo-free starter**,
then checks local reports, `typst init` in an isolated temporary package directory,
both report stages, multiple authors/supervisors, optional publications, and the
minimal layout API. No global package cache is installed or overwritten.

It creates:

```text
dist/academic-uiu-fydp/0.1.0/              Submission files
dist/academic-uiu-fydp-0.1.0.tar.gz        Source archive
dist/academic-uiu-fydp-0.1.0.tar.gz.sha256  Archive checksum
build/package-final.pdf            Logo-free final starter preview
build/package-fydp-1.pdf            Logo-free FYDP-1 preview
```

The package contains only `lib.typ`, `typst.toml`, `README.md`, `LICENSE`, `NOTICE`,
`thumbnail.png`, `template/`, and `docs/`. It excludes `uiu.png`,
the local entry point, build output, scripts, and editor
settings. The thumbnail is a 150 PPI PNG of the initialized cover with a longer
edge exceeding 1080 px and size below 3 MiB.

Normal report PDFs use a fixed creation timestamp through the helper; set
`SOURCE_DATE_EPOCH` if you want a particular build timestamp. The archive checksum
identifies that generated archive; archive metadata is not normalized, so separate
package runs can produce different archive checksums.

## Submit to Typst Universe

1. Fork [typst/packages](https://github.com/typst/packages) on GitHub and clone
   your fork. A sparse checkout is useful because the full repository is large.
2. Create a branch, for example `add-academic-uiu-fydp-0.1.0`.
3. Copy the **contents** of `dist/academic-uiu-fydp/0.1.0/` into
   `packages/preview/academic-uiu-fydp/0.1.0/` in that fork.
4. Commit the package, push your branch, and open a pull request against the
   `main` branch of `typst/packages`.
5. Use the repository's current PR template. Explain the template's purpose,
   attribution, license, tests, and community status. Respond to review feedback.

Suggested description:

> Adds UIU CSE Final Year Design Project Report 0.1.0 for United International University CSE final year design
> project reports. Shaad Ahmmed adapted Swakkhar Shatabda's CC BY 4.0 Overleaf
> LaTeX template to Typst. The package remains CC BY 4.0 and includes attribution
> and a changes notice. It provides editable chapter files, configurable front
> matter, FYDP-1/final variants, and student/educator documentation. No university
> logo is distributed. Local and freshly initialized projects compile with Typst
> 0.15.1. This is a community adaptation without a claim of institutional endorsement.

The import in `template/main.typ` deliberately uses
`@preview/academic-uiu-fydp:0.1.0`, as required for submitted templates. The helper tests
it before publication by staging that namespace locally. Until acceptance, online
users should use the repository's local entry point.

Acceptance is determined by the Universe maintainers, including their licensing
review. CC BY 4.0 is an accepted package license category. The current guidance
also discusses permissively licensed starter scaffolding; this adaptation retains
the original CC BY attribution rather than claiming a new license over inherited
material. Explain its provenance if reviewers ask for licensing adjustments.

## After acceptance

Test the public package:

```sh
typst init @preview/academic-uiu-fydp:0.1.0 my-fydp
cd my-fydp
typst compile main.typ report.pdf
```

Confirm the Universe page and thumbnail, then update the README publication
status and link the actual repository/package page. Share the student and educator
guides with your class. Tag the source release `v0.1.0` if you maintain a source
repository. Creating a GitHub release alone does not publish a Universe package.

## Future versions

Update the manifest version, the starter's import, README examples, documentation,
and workflow artifact name where necessary. Keep the compiler pin and CI version
in sync if raising the minimum compiler. Regenerate the thumbnail and package,
test again, and submit a new version directory. Preserve old published versions.
