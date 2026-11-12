# starship

- **Upstream:** <https://github.com/starship/starship> · <https://starship.rs>
- **Version:** 1.27.0 (2026-10-17)
- **License:** ISC
- **COPR package:** `starship`

A minimal, fast and infinitely customisable prompt for any shell. Spec history
starts with Artem Polishchuk's packaging (maintained in the `atim` COPR), which
is where this file came from; it has since been updated and restructured here.

## Build notes

- Rust package, edition 2024. `Cargo.toml` declares `rust-version = 1.95`;
  Fedora 44 and 45 both ship rust/cargo 1.99, so the requirement is satisfiable
  from the distribution without a toolchain download.
- Built with `cargo build --release --locked` against the `Cargo.lock` in the
  release tarball. This needs crates.io at build time, which the COPR project
  allows (`enable_net`); there is no vendored crate tarball because the
  dependency tree is 418 crates and vendoring it would dwarf the package.
- `--locked` is deliberate: without it cargo silently resolves newer
  dependencies than the release was tested with.
- The binary's own `completions` subcommand generates the bash, zsh and fish
  completions during `%install`, so they cannot drift from the shipped version.
- Previously the spec used `cargo install --root=%{buildroot}%{_prefix}`, which
  writes `.crates.toml`/`.crates2.json` managed-files metadata into `/usr` (the
  old spec had to delete them) and ignores the lockfile.
- `cmake3` and the `openssl`/`zlib` build requirements from the original spec
  were dropped: nothing in the current dependency graph is built with cmake, and
  TLS/compression come from pure-Rust crates (`gix`, `zlib-rs`).

## Testing performed

- SRPM and binary RPM build for Fedora 44 and Fedora 45 (x86_64).
- `dnf install` in a clean container, `starship --version`, `starship print-config`,
  and a real prompt render with `SHELL=/bin/bash` plus a git repository in `$PWD`.
- Upgrade from 1.23.0 (the previously published build) and `rpm -e` clean removal.
