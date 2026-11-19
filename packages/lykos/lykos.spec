%global debug_package %{nil}

Name:           lykos
Version:        0.4.0
Release:        0.7.beta1%{?dist}
Summary:        Fast native music player for GNOME on the Amarok 1.4 layout
License:        GPL-3.0-or-later
URL:            https://github.com/corngoblin/lykos_beta

# The upstream repository is private while the beta is in progress, so COPR
# cannot fetch it: the SRPM carries a `git archive --prefix=lykos-0.4.0/`
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

# Fedora 45 no longer defines the desktop-file-utils scriptlet macros
# (%desktop_database_post and friends), so they would ship as literal text and
# bash would try to run them as job specs: "fg: no job control" on every erase.
# The commands are written out and guarded instead; both are optional runtime
# tools, not requirements.
%post
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
    %{_bindir}/gtk-update-icon-cache -q -t -f %{_datadir}/icons/hicolor >/dev/null 2>&1 || :
fi
if [ -x %{_bindir}/update-desktop-database ]; then
    %{_bindir}/update-desktop-database -q %{_datadir}/applications >/dev/null 2>&1 || :
fi

%postun
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
    %{_bindir}/gtk-update-icon-cache -q -t -f %{_datadir}/icons/hicolor >/dev/null 2>&1 || :
fi
if [ -x %{_bindir}/update-desktop-database ]; then
    %{_bindir}/update-desktop-database -q %{_datadir}/applications >/dev/null 2>&1 || :
fi

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
* Thu Nov 19 2026 corngoblin <corngoblin@users.noreply.github.com> - 0.4.0-0.7.beta1
- Optional three-column browser (artists / albums / tracks) in the style of
  Daphne: chained selection, multi-select with an "N selected" chip, per-column
  search and sortable headings. Default stays the tree.

* Thu Nov 19 2026 corngoblin <corngoblin@users.noreply.github.com> - 0.3.0-0.6.beta1
- Real compositor blur via CSS backdrop-filter (GTK 4.21.2) and
  ext-background-effect-v1 (GTK 4.23.3); the hand-rolled blur painting is gone.
- The blur sits on a dedicated layer behind the content, so text is never part
  of the filtered group.
- Blur amount and tint brightness sliders, alongside the existing tint.
- Album art on collection rows with a live size slider, decoded on a worker.

* Thu Nov 19 2026 corngoblin <corngoblin@users.noreply.github.com> - 0.2.0-0.5.beta1
- Fix the config migration cutoff: v1 stored 0.34, which sat above the 0.30
  threshold, so the very configs that showed the blinding tint would not have
  been migrated. Covered by a unit test now.

* Thu Nov 19 2026 corngoblin <corngoblin@users.noreply.github.com> - 0.2.0-0.4.beta1
- Sidebar glass: the film follows the theme instead of the text colour, so a
  dark theme gets smoked glass instead of a bright wash; blur radius 90.
- The header bar stays opaque inside a transparent window.
- Optional blur for the player bar and the status bar, plus a corner cover
  thumbnail, all with switches in Appearance.
- Playing from the collection now repopulates the playlist table immediately.
- Clear-playlist button with confirmation; clearing resets now-playing and
  persists, so an abrupt quit no longer brings the queue back.
- Library scans show a determinate progress bar with a percentage.
- Preferences pages are titled (the switcher rendered blank icons before).

* Thu Nov 19 2026 corngoblin <corngoblin@users.noreply.github.com> - 0.1.0-0.3.beta1
- Replace the desktop-file-utils scriptlet macros with explicit guarded
  commands: Fedora 45 does not define them, so erase printed
  "fg: no job control" from the unexpanded text.

* Thu Nov 19 2026 corngoblin <corngoblin@users.noreply.github.com> - 0.1.0-0.2.beta1
- Files browser fills when the page opens; one navigation path for the rail
  and the View menu.
- `lykos PATH` queues the tracks under a file or folder, like `exaile LOCATION`.
- Measured performance documented against Exaile 4.2.2.

* Thu Nov 19 2026 corngoblin <corngoblin@users.noreply.github.com> - 0.1.0-0.1.beta1
- First beta: SQLite library, Amarok 1.4 interface, GStreamer playback with
  gapless handoff, MPRIS2, native Wayland blur with an opaque fallback,
  M3U/PLS/XSPF/ASX playlists, lyrics and internet radio.
