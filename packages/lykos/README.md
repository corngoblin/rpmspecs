# lykos

Native GNOME music player: Rust + GTK4/libadwaita, built on Exaile's feature
set and the Amarok 1.4 layout. Upstream: `github.com/corngoblin/lykos_beta`
(private during the beta).

## Why the Fedora 45 floor

The sidebar uses GTK's background-blur path (`Snapshot::push_blur`, reported to
the compositor as `ext-background-effect-v1`). That API is GTK 4.24, which is
Fedora 45; the source does not compile against 4.22. The package is therefore
built for `fedora-45-x86_64` only, deliberately — a Fedora 44 build would fail
at compile time, and a build with the feature removed would not be the
application the user asked for.

## How it is published

The upstream repository is private, so COPR's SCM build cannot fetch it. The
SRPM carries a `git archive --prefix=lykos-0.1.0/` tarball as a local
`Source0`, and builds are uploaded:

```bash
# in the lykos_beta checkout
git archive --prefix=lykos-0.1.0/ -o /tmp/lykos-0.1.0.tar.gz HEAD
rpmbuild -bs packaging/lykos.spec --define "_sourcedir /tmp" --define "_srcrpmdir /tmp/srpm"
copr-cli build monkeygold/Emporium /tmp/srpm/lykos-0.1.0-0.1.beta1.fc45.src.rpm \
    --chroot fedora-45-x86_64
```

When the repository opens, `Source0` becomes the archive URL for the release
tag and this directory can be added as an SCM package like the others.

## Layout

- Binary: `/usr/bin/lykos`
- Desktop entry and metainfo: application ID `io.github.corngoblin.Lykos`
- Icons: hicolor scalable plus 128/256/512 PNGs
- Runtime: GStreamer base + good hard requirements (playbin3, decoders,
  equalizer, replaygain, spectrum); bad-free/ugly-free/libav recommended
