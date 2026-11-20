# tztracker

Terror Zone, Diablo Clone, runeword, magic-find and grail tracker for Diablo II:
Resurrected. Rust, GTK4 and libadwaita.

- Upstream: <https://github.com/corngoblin/TzTracker> (**private** while the
  project is in development)
- COPR package: `tztracker` in `monkeygold/Emporium` (source type `upload`)
- Released as `vX.Y.Z` tags; the flatpak and this RPM are cut from the same tag.

## Why this package exists

The flatpak is the sandboxed build and the one users are pointed at. The RPM
installs the same app natively, which is what a Fedora user expects from a
package manager and what keeps the app out of a sandbox when it talks to a game
that is running outside one.

## Building it

Upstream is private, so COPR cannot clone it and the package is **not** SCM.
Every release is submitted from an uploaded SRPM that carries the source
tarball. `scripts/rpm-build.sh` is not used for this package because its
`spectool -g` step needs a `Source0` URL; the flow is:

```sh
# 1. tarball from the tagged commit, prefix must be tztracker-<version>/
git -C ~/Projects/tztracker archive --prefix=tztracker-1.5.4/ v1.5.4 \
    -o ~/rpmbuild-e/f45/SOURCES/tztracker-1.5.4.tar.gz

# 2. spec into the tree and build SRPM + RPM in a fedora:45 container
cp packages/tztracker/tztracker.spec ~/rpmbuild-e/f45/SPECS/
podman exec emporium-f45 rpmbuild -ba --define "_topdir /work" \
    /work/SPECS/tztracker.spec

# 3. publish
copr-cli build monkeygold/Emporium ~/rpmbuild-e/f45/SRPMS/tztracker-1.5.4-1.fc45.src.rpm
```

`BuildRequires` are broad enough that `dnf builddep tztracker.spec` on a bare
Fedora install is all COPR needs. The crate registry is required: the build
uses `cargo build --release --locked` and there is no vendored tarball, so the
project's `enable_net` must stay on.

## Packaging notes

- **`%{?dist}` is set on the SRPM's own release**, so an SRPM built on Fedora 45
  submits correctly to a project that also builds Fedora 44 — COPR rebuilds the
  SRPM per chroot from the spec, and both chroots get their own dist tag.
- **The desktop id is shared with the flatpak** (`io.github.corngoblin.TzTracker`).
  Flatpak's export directory comes first in `XDG_DATA_DIRS`, so with both
  installed the flatpak's launcher wins. Install one or the other; they also share
  the same config and cache directories (`~/.config/tztracker`, …), which is
  intentional — the same app, the same settings.
- **Erase leaves user data behind on purpose.** `~/.config/tztracker`,
  `~/.local/share/tztracker` (bundled sounds are copied there on first run),
  `~/.cache/tztracker` (Terror Zone and Diablo Clone caches) and
  `~/.local/state/tztracker` are the user's, not the package's. A user who wants
  them gone runs `rm -rf ~/.config/tztracker ~/.local/share/tztracker
  ~/.cache/tztracker ~/.local/state/tztracker`. The package itself installs no
  files outside `/usr`, creates no D-Bus service file and no systemd unit, so an
  erase is complete apart from those directories.
- **The bundled notification sounds are MP3**, so `gstreamer1-plugins-good` is a
  Recommends: without it the app runs but cannot play a sound when a favourite
  zone comes up.
