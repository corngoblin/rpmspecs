%global debug_package %{nil}
# The binary is 12 MB stripped; Rust's debuginfo for it is several hundred MB of
# COPR build time and artifact space that nobody installs.

%global app_id io.github.corngoblin.TzTracker

Name:           tztracker
Version:        1.5.4
Release:        1%{?dist}
Summary:        Terror Zone, Diablo Clone and magic-find tracker for Diablo II: Resurrected

License:        GPL-3.0-or-later
URL:            https://github.com/corngoblin/TzTracker

# Local source on purpose: the upstream repository is private, so COPR cannot
# fetch it. The SRPM carries the tarball and every build is submitted with
# `copr-cli build monkeygold/Emporium <srpm>`. When the repository opens,
# replace this with %%{url}/archive/v%{version}/%{name}-%{version}.tar.gz and
# wire the package as SCM with subdirectory packages/tztracker/.
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  rust cargo
BuildRequires:  pkgconfig
BuildRequires:  glib2-devel
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

# GStreamer itself is linked and comes in through the sonames; the decoders are
# not, and the bundled notification sounds are MP3. Without them the app is
# silent instead of broken, so this is a Recommends and not a Requires.
Recommends:     gstreamer1-plugins-good
Recommends:     gstreamer1-plugins-base

%description
TzTracker shows the current Terror Zone in Diablo II: Resurrected with the time
left on it, the rotation that follows, and — since every Terror Zone is a
different place to farm — its monster immunities and its experience and loot
tiers.

It keeps a small always-on-top card that can be dragged anywhere and faded to
taste, so the zone and its countdown stay visible over a borderless-windowed
game, and it can play a sound when a favourite zone comes up.

The rest of the window covers what else a run needs: Diablo Clone progress per
region, the 100 runewords with their runes and bases, the crafting recipes, a
magic-find run counter, a drop calculator for uniques, sets, runes and bases,
a grail checklist, and a Diablo II loot-filter editor.

The Terror Zone and Diablo Clone feeds come from d2tz.info. Diablo Clone
progress needs a free API key from that site; the Terror Zone feed does not.

%prep
%autosetup -n %{name}-%{version}

%build
# The GUI is built on the gtk4 and libadwaita crates, so this needs the crates.io
# registry. COPR has network enabled for this project, and --locked pins every
# crate to Cargo.lock so a build cannot drift silently between releases.
cargo build --release --locked

%install
install -Dpm0755 target/release/tztracker %{buildroot}%{_bindir}/tztracker

install -Dpm0644 data/%{app_id}.desktop %{buildroot}%{_datadir}/applications/%{app_id}.desktop
install -Dpm0644 data/%{app_id}.metainfo.xml %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml

for size in 64 128 256 512; do
    install -Dpm0644 data/icons/hicolor/${size}x${size}/apps/%{app_id}.png \
        %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{app_id}.png
done

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{app_id}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{app_id}.metainfo.xml

# The refresh macros (%desktop_database_post, %icon_theme_cache_post) no longer
# exist in current Fedora, so the commands are written out behind a file test.
# They are best-effort by definition: a missed cache refresh is corrected by the
# next boot or rebuild, while a scriptlet that fails rolls the whole transaction
# back and looks like an uninstallable package.
%post
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache -q -t -f %{_datadir}/icons/hicolor >/dev/null 2>&1 || :
fi
if [ -x /usr/bin/update-desktop-database ]; then
    /usr/bin/update-desktop-database -q %{_datadir}/applications >/dev/null 2>&1 || :
fi

%postun
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache -q -t -f %{_datadir}/icons/hicolor >/dev/null 2>&1 || :
fi
if [ -x /usr/bin/update-desktop-database ]; then
    /usr/bin/update-desktop-database -q %{_datadir}/applications >/dev/null 2>&1 || :
fi

%files
%license LICENSE
%doc README.md
%{_bindir}/tztracker
%{_datadir}/applications/%{app_id}.desktop
%{_metainfodir}/%{app_id}.metainfo.xml
%{_datadir}/icons/hicolor/64x64/apps/%{app_id}.png
%{_datadir}/icons/hicolor/128x128/apps/%{app_id}.png
%{_datadir}/icons/hicolor/256x256/apps/%{app_id}.png
%{_datadir}/icons/hicolor/512x512/apps/%{app_id}.png

%changelog
* Fri Nov 20 2026 corngoblin <corngoblin@users.noreply.github.com> - 1.5.4-1
- First RPM: the tracker page, the in-game overlay, Diablo Clone progress,
  runewords, recipes, the magic-find counter, the drop calculator, the grail
  and the loot-filter editor.
- Rotations are polled around the actual rotation boundary instead of on a blind
  timer, so the next zone appears seconds after the tracker publishes it.
- The overlay window is owned by the application state, so it cannot be created
  twice.
