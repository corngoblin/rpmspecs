%global debug_package %{nil}

Name:           lykos
Version:        0.1.0
Release:        0.2.beta1%{?dist}
Summary:        Fast native music player for GNOME on the Amarok 1.4 layout
License:        GPL-3.0-or-later
URL:            https://github.com/corngoblin/lykos_beta

# The upstream repository is private while the beta is in progress, so COPR
# cannot fetch it: the SRPM carries a `git archive --prefix=lykos-0.1.0/`
# tarball instead. When the repository opens, Source0 becomes the archive URL
# for the release tag and nothing else in this spec changes.
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  pkgconfig
# Blur is a GTK 4.24 API (Snapshot::push_blur gated by the background-blur
# protocol); the source does not compile against 4.22. Fedora 45 is the floor.
BuildRequires:  gtk4-devel >= 4.24
BuildRequires:  libadwaita-devel >= 1.8
BuildRequires:  gstreamer1-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  gtk-update-icon-cache

# GStreamer runtime: playbin3, vorbis/opus/mp3/flac decoders and the elements
# the equalizer, ReplayGain and the analyser are built from.
Requires:       gstreamer1-plugins-base
Requires:       gstreamer1-plugins-good
Recommends:     gstreamer1-plugins-bad-free
Recommends:     gstreamer1-plugins-ugly-free
Recommends:     gstreamer1-plugins-libav

%description
Lykos plays a local music library with the layout Amarok 1.4 made familiar: a
browser column down the left, the playlist and its transport bar on the right,
and a context pane with the cover, the metadata and the lyrics of what is
playing.

The library is a SQLite index, so browsing, filtering and smart playlists stay
fast with tens of thousands of tracks. Tags are read on worker threads, cover
art is decoded off the main loop, and the playlist table only builds the rows
that are on screen.

On Wayland with GTK 4.24 or newer the sidebar uses the compositor's native
background blur; elsewhere it falls back to an opaque panel.

%prep
%autosetup -n %{name}-%{version}

%build
# --locked pins every crate to Cargo.lock so a build cannot drift.
cargo build --release --locked

%install
install -Dpm0755 target/release/lykos %{buildroot}%{_bindir}/lykos

install -Dpm0644 data/io.github.corngoblin.Lykos.desktop \
    %{buildroot}%{_datadir}/applications/io.github.corngoblin.Lykos.desktop
install -Dpm0644 data/io.github.corngoblin.Lykos.metainfo.xml \
    %{buildroot}%{_metainfodir}/io.github.corngoblin.Lykos.metainfo.xml

install -Dpm0644 data/io.github.corngoblin.Lykos.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/io.github.corngoblin.Lykos.svg
install -Dpm0644 data/io.github.corngoblin.Lykos-512.png \
    %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/io.github.corngoblin.Lykos.png
install -Dpm0644 data/io.github.corngoblin.Lykos-256.png \
    %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/io.github.corngoblin.Lykos.png
install -Dpm0644 data/io.github.corngoblin.Lykos-128.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/io.github.corngoblin.Lykos.png

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/io.github.corngoblin.Lykos.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/io.github.corngoblin.Lykos.metainfo.xml

%post
%desktop_database_post || :
%icon_theme_cache_post || :

%postun
%desktop_database_postun || :
%icon_theme_cache_postun || :

%files
%license LICENSE
%doc README.md docs/01-exaile-audit.md docs/02-architecture.md docs/03-feature-matrix.md docs/04-ui-layout.md docs/05-performance.md
%{_bindir}/lykos
%{_datadir}/applications/io.github.corngoblin.Lykos.desktop
%{_metainfodir}/io.github.corngoblin.Lykos.metainfo.xml
%{_datadir}/icons/hicolor/scalable/apps/io.github.corngoblin.Lykos.svg
%{_datadir}/icons/hicolor/512x512/apps/io.github.corngoblin.Lykos.png
%{_datadir}/icons/hicolor/256x256/apps/io.github.corngoblin.Lykos.png
%{_datadir}/icons/hicolor/128x128/apps/io.github.corngoblin.Lykos.png

%changelog
* Thu Nov 19 2026 corngoblin <corngoblin@users.noreply.github.com> - 0.1.0-0.2.beta1
- Files browser fills when the page opens; one navigation path for the rail
  and the View menu.
- `lykos PATH` queues the tracks under a file or folder, like `exaile LOCATION`.
- Measured performance documented against Exaile 4.2.2.

* Thu Nov 19 2026 corngoblin <corngoblin@users.noreply.github.com> - 0.1.0-0.1.beta1
- First beta: SQLite library, Amarok 1.4 interface, GStreamer playback with
  gapless handoff, MPRIS2, native Wayland blur with an opaque fallback,
  M3U/PLS/XSPF/ASX playlists, lyrics and internet radio.
