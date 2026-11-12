# uzdoom

- **Upstream:** <https://github.com/UZDoom/UZDoom>
- **Version:** 5.0.3 (2026-09-23)
- **License:** GPL-3.0-or-later
- **Replaces:** the retired `gzdoom` package in Emporium

UZDoom is the continuation of GZDoom (which in turn continues ZDoom): a Doom
engine source port with OpenGL and Vulkan renderers, 3D floors, dynamic lights
and ZScript modding. It covers Doom, Doom II, Heretic, Hexen, Strife and
fan-made games from the idTech 1 family.

## Why this replaced gzdoom

The `gzdoom` package could not be built in Emporium at all: its spec declared
`BuildRequires: zmusic-devel` and `Requires: zmusic`, and neither package exists
in Fedora — the `zmusic` package in the same repository was never resolvable to
the gzdoom build either. UZDoom vendors ZMusic and every audio backend in-tree,
so the pair of interdependent packages collapses into one self-contained spec.

## Build notes

- CMake build, `-DBUILD_NONFREE=OFF`. Upstream's "nonfree" directory contains
  widescreen graphics, brightmaps and fonts *based on original commercial game
  content*; excluding them keeps the package entirely GPL. See `LICENSING.md`.
- `-DFORCE_NO_LTO=ON` plus `%global _lto_cflags %{nil}`: the engine builds ~1600
  translation units of its own static libraries, and a distribution-wide LTO pass
  only multiplies build time (and memory use on COPR builders).
- The release tarball has no git metadata, so `%build` exports
  `GIT_DESCRIBE=%{version}`; without it the in-game version string reads
  "unknown" and bug reports are unusable.
- Installed layout: `/usr/bin/uzdoom`, game resources and the bundled soundfonts
  in `/usr/share/games/uzdoom/`, docs in `/usr/share/doc/uzdoom/`, plus the
  upstream desktop entry, metainfo, icon and mime definition.
- OpenAL is `dlopen()`ed at runtime and GL/Vulkan drivers are loaded by the
  driver stack, so `openal-soft` is an explicit `Requires` and `vulkan-loader`
  and `freedoom` are `Recommends`.

## Runtime

No game data ships in the package. `uzdoom` needs an IWAD: either one from a
game you own, or the freely distributable Freedoom (`dnf install freedoom`), or
you can drag a `.wad`/`.pk3` onto the launcher.

## Testing performed

- Builds for Fedora 44 and Fedora 45 (x86_64) with `scripts/rpm-build.sh`.
- Install / `--version` / `-iwad` launch smoke test in a clean container.
- Upgrade over the previously published package and `rpm -e` clean removal.
