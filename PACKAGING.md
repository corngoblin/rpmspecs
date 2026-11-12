# Packaging conventions

One directory per source package, `packages/<name>/`, containing everything
needed to rebuild that package: the spec, its patches, and any packaging assets
(desktop entries, icons) that upstream does not ship itself. A short `README.md`
in each directory records the upstream project, why the package exists and any
deviation from upstream defaults.

## Spec rules

- **SPDX license identifiers.** `GPLv3+` and friends are not valid SPDX and fail
  current Fedora review. Touch a spec, convert its license tag.
- `%autosetup` (with `-n` only when the archive prefix differs from
  `%{name}-%{version}`).
- `Release: 1%{?dist}` — the dist tag tells a Fedora 44 RPM from a Fedora 45
  one, and an untagged release silently masquerades as a generic build.
- `Source0` points at an official upstream release artifact with `%{version}` in
  it, never at a file in this repository and never at a `master`/`main` snapshot
  that moves underneath us.
- **Nothing is fetched at spec-parse time.** `%global foo %(curl …)` makes the
  build depend on the state of the network at parse time and silently produces an
  empty value when the API rate-limits. Resolve versions by hand when bumping.
- Pin commits that are fetched from git to a full 40-character hash. A 43-character
  hash is a typo that `%forgemeta` hides until the tag it resolves disappears.
- `BuildRequires` must be complete enough that `dnf builddep <spec>` on a bare
  Fedora install is sufficient; that is exactly what COPR does.
- Do not hand-write `Requires` for shared libraries. Let the automatic dependency
  generator add sonames; spell out only what it cannot see — binaries and data the
  application *runs*, `dlopen()`ed libraries, and plugin sets.
- `Recommends` for optional runtime that a minimal install should not be forced
  to pull in (freedoom for uzdoom, vulkan-loader, extra decoders).
- Cache refreshes in scriptlets are best-effort: `… &>/dev/null || :`.
- Every change gets a changelog entry with a version bump, including packaging-only
  changes (bump `Release`).

## Building and testing

```bash
scripts/rpm-build.sh 44 <package>          # build in a clean fedora:44 container
scripts/rpm-build.sh 45 <package>
scripts/rpm-build.sh 45 <package> --test-install
```

Checklist for anything being published (all of it, not a subset):

1. `rpmspec -P` parses, `rpmlint` is clean apart from known-benign noise.
2. SRPM builds and binary RPMs build for **both** Fedora 44 and 45.
3. `rpm -qpl` shows what you expect; no stray build directories, no missing
   `.desktop` file, no unpackaged files.
4. `rpm -qpR` requirements resolve on a bare Fedora install.
5. `dnf install` on a clean container, then the application actually starts
   (for a GUI: `--version` plus a headless launch under `Xvfb`/`weston`).
6. Upgrade from the previously published version with `dnf upgrade <rpm>`.
7. `rpm -e` leaves no files behind and reports no scriptlet failures.

## COPR wiring

Every published package is an SCM package pointing at this repository
(`https://github.com/corngoblin/rpmspecs`, branch `main`) with:

- `subdirectory`: `packages/<name>/`
- `spec`: `<name>.spec`
- build method `rpkg`

Changing a directory name therefore requires `copr-cli edit-package-scm`
for the affected package; a build that fails with "no spec file found" almost
always means the COPR package still points at an old path.

Add a package:

```bash
copr-cli add-package-scm monkeygold/Emporium --name <pkg> \
    --clone-url https://github.com/corngoblin/rpmspecs --commit main \
    --subdir packages/<pkg>/ --spec <pkg>.spec --method rpkg
copr-cli build-package monkeygold/Emporium --name <pkg>
```

## Version bumps

1. `gh api repos/<owner>/<repo>/releases/latest --jq .tag_name` — or, for rolling
   projects (DuckStation-style), the newest tag rather than the release object.
2. Update `Version`, `Source0`, and any pinned toolchain (`%global zigver` for
   ghostty, the Rust floor for starship) in the same commit.
3. Build for 44 and 45, install-test, then publish.
4. Keep `README.md`'s version table in step with the spec — the table is a claim
   about what Emporium serves.
