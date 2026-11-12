# Licensing notes

Packaging a program means redistributing it, so the license has to permit
redistribution of a *built* artifact, not just of the source. Two packages need
a note; the rest are straightforward.

## DuckStation — not packaged, not published

Removed from Emporium and from this repository on 2026-11-12. It is not an
oversight and it is not a build problem we gave up on: upstream forbids it.

- License is **CC-BY-NC-ND-4.0** — non-commercial, and *no derivatives*.
- `README.md`, upstream: *"pre-configured settings and packages are considered
  modifications"* and *"You are not permitted to publish modified versions of this
  repository."*
- `CMakeLists.txt`, lines 1-6, upstream: the build files carry a **Packaging
  Restriction** on top of CC-BY-NC-ND — *"you may not use this file to create
  packages or build recipes without explicit permission from the copyright
  holder."*

A distro RPM is exactly what both sentences prohibit: a package, carrying a build
recipe, redistributing a build of "modified" (configured, patched, linked against
system libraries) source. Publishing one to a public COPR would be a license
violation, so there is no DuckStation spec here — writing one is itself what the
restriction forbids. A private local build would still be a build recipe.

Legitimate ways to run DuckStation on Fedora:

- the official AppImage from <https://www.duckstation.org/>
- the official Flatpak (`org.duckstation.DuckStation`) from upstream's own
  Flathub listing

Both come from the copyright holder, which is what CC-BY-NC-ND permits.
If permission is ever granted in writing, the packaging work can be redone — the
prior research (CMake build, bundled `dep/` tree, Qt6/SDL3 requirements) is in the
project history.

## UZDoom — GPL-3.0-or-later, built without the non-free assets

UZDoom's engine is GPL-3.0-or-later and is redistributable. Upstream also ships
"nonfree" assets (`wadsrc_extra/nonfree`, brightmaps, widescreen graphics) that
are *based on original commercial game content*; their own `license.md` restricts
them to non-commercial use tied to the game they came from.

The spec therefore builds with `-DBUILD_NONFREE=OFF`. The package contains only
GPL content, and the widescreen graphics / brightmaps / extra fonts those files
provide are the visible difference. Engine functionality is unaffected.

UZDoom vendors ZMusic and its audio backends (FluidSynth, GME, WildMIDI, libxmp,
ADLMIDI, OPNMIDI, dumb, Timidity, oplsynth) in-tree and links them statically.
They are declared with `Provides: bundled(...)` in the spec, as Fedora requires
for bundled libraries, and no source is downloaded during the build.

## Everything else

| Package | License |
|---|---|
| ghostty | MIT |
| starship | ISC |
| lact, lact-headless | MIT |
| nautilus-open-any-terminal | GPL-3.0-or-later |
| topgrade | GPL-3.0-only |
| twad | MIT |
| woeusb-ng | GPL-3.0-or-later |
| copyparty | MIT |
| sunshine | GPL-3.0-only |
| ymir | GPL-3.0-or-later |

Emporium's own description says it plainly: *"THERE IS NO SUPPORT USING ANYTHING
IN THIS REPO."* Nothing here is reviewed by Fedora; it is a personal repository.
