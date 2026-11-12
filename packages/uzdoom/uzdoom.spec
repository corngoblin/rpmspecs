%global debug_package %{nil}

# The engine already builds its own static libraries; a distribution-wide LTO
# pass over 1600 translation units only doubles build time here.
%global _lto_cflags %{nil}

Name:           uzdoom
Version:        5.0.3
Release:        1%{?dist}
Summary:        Modern Doom engine source port supporting Doom, Heretic, Hexen and Strife

# Upstream states GPLv3 or later. The engine ships no game data: an IWAD from a
# commercially released game (or freedoom) is required at runtime.
License:        GPL-3.0-or-later
URL:            https://github.com/UZDoom/UZDoom
Source0:        %{url}/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz

# UZDoom vendors its dependencies in-tree (libraries/) because they are either
# not packaged in Fedora or are patched forks. ZMusic and its audio backends are
# built statically into the binary; nothing is downloaded during the build.
Provides:       bundled(zmusic) = 1.3.0
Provides:       bundled(fluidsynth)
Provides:       bundled(game-music-emu)
Provides:       bundled(wildmidi)
Provides:       bundled(libxmp)
Provides:       bundled(libADLMIDI)
Provides:       bundled(libOPNMIDI)
Provides:       bundled(dumb)
Provides:       bundled(timidity++)
Provides:       bundled(oplsynth)
Provides:       bundled(asmjit)
Provides:       bundled(abseil-cpp)
Provides:       bundled(cppdap)
Provides:       bundled(ZVulkan)
Provides:       bundled(ZWidget)
Provides:       bundled(miniz)
Provides:       bundled(lzma-sdk)
Provides:       bundled(range_map)

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  pkgconfig(sdl2)
# The bundled FluidSynth and ZMusic audio backends link against GLib and ALSA.
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(vpx)
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

Requires:       hicolor-icon-theme
# OpenAL and the GL/Vulkan drivers are opened with dlopen(), so they are not
# picked up by the automatic soname dependency generator.
Requires:       openal-soft
Recommends:     freedoom
Recommends:     vulkan-loader

%description
UZDoom is a modern, feature-rich source port of the Doom engine, continuing the
ZDoom and GZDoom lineage. It runs Doom, Doom II, Heretic, Hexen, Strife and
fan-made games built on the idTech 1 family of engines.

Features include an OpenGL and a Vulkan renderer, high resolutions, 3D floors,
dynamic lights, full ZScript modding support, and several built-in softsynths
for MUS and MIDI playback (OPL, GUS, FluidSynth, WildMIDI, Timidity).

No game data is included: you need the IWAD of a game you own, or the freely
distributable Freedoom IWADs from the freedoom package.

%prep
%autosetup -n UZDoom-%{version}

%build
# The release tarball carries no git metadata; tell the build what version it is
# building so the in-game version string and bug reports are meaningful.
export GIT_DESCRIBE=%{version}

# BUILD_NONFREE=OFF: upstream's "nonfree" assets (widescreen graphics, brightmaps
# and fonts derived from commercially released game data) are excluded so the
# package contains only content that is redistributable under the GPL.
%cmake -GNinja \
       -DCMAKE_BUILD_TYPE=Release \
       -DBUILD_NONFREE=OFF \
       -DFORCE_NO_LTO=ON \
       -DDYN_OPENAL=ON \
       -DNO_STRIP=ON \
       -DINSTALL_PK3_PATH=%{_datadir}/games/%{name} \
       -DINSTALL_SOUNDFONT_PATH=%{_datadir}/games/%{name} \
       -DINSTALL_DOCS_PATH=%{_docdir}/%{name}
%cmake_build

%install
%cmake_install

# Upstream installs the launcher and mime package itself; validate rather than copy.
desktop-file-validate %{buildroot}%{_datadir}/applications/org.zdoom.UZDoom.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/org.zdoom.UZDoom.metainfo.xml

# Icon cache, desktop database and mime database are refreshed by the
# transfiletriggers shipped in hicolor-icon-theme, desktop-file-utils and
# shared-mime-info, so this package does not need scriptlets of its own.

%files
%license LICENSE
%doc %{_docdir}/%{name}
%{_bindir}/uzdoom
%{_datadir}/games/%{name}/
%{_datadir}/applications/org.zdoom.UZDoom.desktop
%{_datadir}/icons/hicolor/scalable/apps/org.zdoom.UZDoom.svg
%{_metainfodir}/org.zdoom.UZDoom.metainfo.xml
%{_datadir}/mime/packages/org.zdoom.UZDoom-mime.xml

%changelog
* Thu Nov 12 2026 Ferah <ferah@localhost> - 5.0.3-1
- Initial package: UZDoom 5.0.3, replacing the retired gzdoom package
