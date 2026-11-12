# rpmspecs

RPM packaging sources for the **Emporium** COPR project
([`monkeygold/Emporium`](https://copr.fedorainfracloud.org/coprs/monkeygold/Emporium/)).

`Emporium` is a personal repository. A lot of these specs were not written here:
they were sourced from other places and people, for the sole reason of cleaning
up a long repo list and having a single repository to add to a Fedora system.
They are maintained here now, and this repository is the source of truth — COPR
builds each package straight from a directory below (`packages/<name>/`), so a
change lands here before it reaches anyone's package manager.

Builds target **Fedora 44 and Fedora 45** only, `x86_64` and `aarch64`.

## Layout

```
packages/<name>/        one directory per source package
    <name>.spec         the spec COPR builds
    *.patch             patches applied by the spec, if any
    *.desktop, *.png    packaging assets upstream does not ship
    README.md           what the package is, where it comes from, how it is built
archive/                retired packaging, kept for reference only (not built)
scripts/rpm-build.sh    build and install-test one package in a clean container
PACKAGING.md            conventions every spec here follows
LICENSING.md            licensing notes, including what we cannot ship
```

## Packages

| Directory | Package(s) | Upstream | Version | COPR |
|---|---|---|---|---|
| `packages/ghostty` | ghostty | [ghostty-org/ghostty](https://github.com/ghostty-org/ghostty) | 1.4.0 | `ghostty` |
| `packages/starship` | starship | [starship/starship](https://github.com/starship/starship) | 1.27.0 | `starship` |
| `packages/uzdoom` | uzdoom | [UZDoom/UZDoom](https://github.com/UZDoom/UZDoom) | 5.0.3 | `uzdoom` |
| `packages/lact` | lact, lact-headless | [ilya-zlobintsev/LACT](https://github.com/ilya-zlobintsev/LACT) | 0.8.2 | `lact`, `lact-headless` |
| `packages/nautilus-open-any-terminal` | nautilus-open-any-terminal | [Stunkymonkey/nautilus-open-any-terminal](https://github.com/Stunkymonkey/nautilus-open-any-terminal) | 0.6.3 | `nautilus-open-any-terminal` |
| `packages/topgrade` | topgrade | [topgrade-rs/topgrade](https://github.com/topgrade-rs/topgrade) | 16.0.4 | `topgrade` |
| `packages/twad` | twad | [twad-rs/twad](https://github.com/twad-rs/twad) | 0.30.0 | `twad` — never built, see below |
| `packages/woeusb-ng` | woeusb-ng | [WoeUSB/WoeUSB-ng](https://github.com/WoeUSB/WoeUSB-ng) | 0.2.10 | `woeusb-ng` — never built, see below |
| `packages/sunshine` | sunshine | [LizardByte/Sunshine](https://github.com/LizardByte/Sunshine) | 2025.628.4510 | not published |
| `packages/ymir` | ymir | [StrikerX3/Ymir](https://github.com/StrikerX3/Ymir) | 0.1.7 | not published |

`archive/` holds `gzdoom` only — superseded by `uzdoom`, patches kept for
reference. The DuckStation and ghostty-nightly specs were removed rather than
archived: the first is a licence issue (see `LICENSING.md`), the second resolved
its commit with a `curl` at spec-parse time.

## Building

```bash
# build for Fedora 45 in a clean container (deps, sources, RPMs)
scripts/rpm-build.sh 45 uzdoom

# the same, plus install the result in a throwaway container
scripts/rpm-build.sh 45 uzdoom --test-install
```

Artifacts land in `~/rpmbuild-e/f<NN>/{RPMS,SRPMS}`. The script installs the
spec's `BuildRequires` with `dnf builddep`, so a missing build dependency fails
in the same place COPR would hit it.

Publishing is a separate, deliberate step:

```bash
copr-cli build-package monkeygold/Emporium --name uzdoom
```

## Known gaps

- `twad` and `woeusb-ng` are configured in COPR but have **never had a single
  build**: `twad` fetches Go modules at build time without vendoring, and
  `woeusb-ng` points `Source0` at a tarball that is not in the repository.
- `ymir` has no usable `Source0` and is not published.
- `sunshine` and `ymir` are not part of Emporium's build set; they live here
  because this is where packaging belongs.
