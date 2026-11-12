# ghostty

- **Upstream:** <https://github.com/ghostty-org/ghostty> · <https://ghostty.org>
- **Version:** 1.4.0 (tag `v1.4.0`)
- **License:** MIT
- **COPR package:** `ghostty`

A GPU-accelerated terminal emulator with a native GTK4/libadwaita frontend.
Zig build system, no autotools/cmake anywhere.

## The Zig version problem

Ghostty pins the exact Zig release it is developed against — `minimum_zig_version`
in `build.zig.zon`, `0.17.0` for 1.4.0 — and upstream CI installs precisely that
version. Fedora 44 and 45 both ship Zig 0.16, which is too old and fails the build
immediately.

The spec therefore downloads the official Zig release from `ziglang.org`
(`Source1`/`Source2`, one per architecture, extracted into the build directory and
put first in `PATH`) instead of using the distribution's `zig`. This keeps the
build reproducible and avoids a Fedora-version-dependent toolchain. When bumping
Ghostty, read the new `minimum_zig_version` and update `%global zigver` in the
same commit — the build refuses to proceed otherwise.

## Build notes

- `zig build -Doptimize=ReleaseFast -Dcpu=baseline -Dpie=true -Demit-docs`.
  `-Dcpu=baseline` keeps the binary portable across the arch's CPUs,
  `-Dpie=true` produces a hardened PIE, `-Demit-docs` generates the man pages
  from upstream's docs (hence `pandoc-cli`).
- Ghostty's Zig dependencies (libxev, vaxis, zigimg, the Wayland and GTK
  bindings, JetBrains Mono and the Nerd Fonts symbols, the theme bundle) are the
  hash-pinned tarballs listed in `build.zig.zon` and are fetched from
  `deps.files.ghostty.org` during the build. The COPR project has network access
  enabled for builds; nothing is fetched at spec-parse time.
- The `%install` pass re-runs the same `zig build` with `DESTDIR` set, so the
  compile in `%build` is cached and `%{buildroot}` is never touched early.
- The packaged terminfo entry is `xterm-ghostty` only. `share/terminfo/g/ghostty`
  is deleted from the buildroot because `ncurses-base` owns that name on Fedora 42
  and newer, and two packages owning one path is a transaction failure waiting for
  the first upstream change.
- `desktop-file-validate` runs during the build; a malformed desktop entry fails
  the build instead of shipping.

## Testing performed

- SRPM and binary RPM build for Fedora 44 and Fedora 45 (x86_64), with the Zig
  toolchain fetched from the sources above.
- `dnf install` in a clean container, `ghostty +version`, `ghostty +show-config`
  and `ghostty +list-themes`.
- Headless launch under `Xvfb` (GTK4 needs a display; the app must open a window
  and exit cleanly on SIGTERM without criticals).
- Upgrade from 1.2.2 and `rpm -e` clean removal.
