Name:           gzdoom
Version:        4.14.2
Release:        1%{?dist}
Summary:        An OpenGL DOOM source port with graphic and modding extensions
License:        GPLv3
Url:            http://zdoom.org
Source0:        https://github.com/ZDoom/gzdoom/archive/g4.14.2.tar.gz
Source1:        gzdoom.desktop

Provides:       zdoom = 2.8.1
Provides:       qzdoom = 1.3.0
Provides:       bundled(re2c) = 0.16.0
Provides:       bundled(gdtoa)
#Provides:       bundled(lzma-sdk) = 17.01
#Provides:       bundled(dumb) = 0.9.3

Patch1:         %{name}-waddir.patch
Patch2:         %{name}-asmjit.patch
Patch3:         %{name}-fix-gcc15.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  cmake
BuildRequires:  tar
BuildRequires:  git
BuildRequires:  nasm
BuildRequires:  glew-devel
BuildRequires:  pkgconfig(libwebp)

# Todo: Patch
#BuildRequires:  glslang-devel

# pkgconfig
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(fluidsynth)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(sdl)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(libgme)
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(libmpg123)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(vpx)

BuildRequires:  timidity++
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(wildmidi)
Requires:       wildmidi

Requires:       openal-soft
Requires:       fluidsynth
Requires:       SDL2

# ZMusic Requirement
BuildRequires:  zmusic-devel
Requires:       zmusic

Recommends:     freedoom

%description
ZDoom is a family of enhanced ports (modifications) of the Doom engine for
running on modern operating systems. It runs on Windows, Linux, and OS X, and
adds new features not found in the games as originally published by id Software.

ZDoom features the following that is not found in the original Doom:

  * Runs on all modern versions of Windows, Mac, and Linux distributions
  * Can play all Doom engine games, including Ultimate Doom, Doom II, Heretic,
    Hexen, Strife, and more
  * Supports all editing features of Hexen
  * Supports most of the Boom editing features
  * Supports new features such as colored lighting, 3D floors, and much more
  * All Doom limits are gone
  * Several softsynths for MUS and MIDI playback, including OPL softsynth for an
    authentitc "oldschool" flavor
  * High resolutions
  * Quake-style console and key bindings
  * Crosshairs
  * Free look
  * Jumping, crouching, swimming, and flying
  * Up to 8 player network games using UDP/IP, including team-based gameplay
  * Support for the Bloodbath announcer from the classic Monolith game Blood
  * Walk over/under monsters and other things

GZDoom provides an OpenGL renderer and HQnX rescaling.

%prep
%setup -q -n %{name}-g4.14.2
%patch -P 1 -P 2 -P 3 -p1

perl -i -pe 's{__DATE__}{""}g' \
        src/common/platform/posix/sdl/i_main.cpp
perl -i -pe 's{<unknown version>}{%{version}}g' \
        tools/updaterevision/UpdateRevision.cmake

%build
%define _lto_cflags %nil
export _rhel_flags="-fPIC"

%cmake  -B builddir \
        -DNO_STRIP=1 \
        -DCMAKE_C_FLAGS="$_rhel_flags" -DCMAKE_CXX_FLAGS="$_rhel_flags" \
        -DCMAKE_SHARED_LINKER_FLAGS="" \
        -DCMAKE_EXE_LINKER_FLAGS="" \
        -DCMAKE_MODULE_LINKER_FLAGS="" \
        -DBUILD_SHARED_LIBS="OFF" \
        -DINSTALL_DOCS_PATH="%{_docdir}/%{name}" \
        -DINSTALL_PK3_PATH="%{_datadir}/doom" \
        -DCMAKE_BUILD_TYPE=RelWithDebInfo

make %{?_smp_mflags} -C builddir

%install
rm -rf $RPM_BUILD_ROOT

# Install gzdoom
%make_install -C builddir

%{__mkdir} -p %{buildroot}%{_datadir}/applications
%{__install} -m 0644 %{SOURCE1} \
  %{buildroot}%{_datadir}/applications/gzdoom.desktop

# Don't know why but the XPM isn't put anywhere
%{__mkdir} -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
cp %{_builddir}/%{name}-g4.14.2/src/posix/zdoom.xpm \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/gzdoom.xpm

# Fallback soundfont - Symlinking instead of copying
# as a test for now. It's not clear if the binary will look here
# or look in /usr/share/games/doom yet.
pushd %{buildroot}%{_datadir}/doom
    %{__ln_s} %{_datadir}/games/doom/soundfonts soundfonts
    %{__ln_s} %{_datadir}/games/doom/fm_banks fm_banks
popd

%post
echo "INFO: %{name}: The global IWAD directory is %{_datadir}/doom."

%files
%defattr(-, root, root, -)
%doc docs/console.css docs/console.html docs/rh-log.txt docs/licenses/* docs/skins.txt
%{_bindir}/%{name}
%{_datadir}/doom/*
%{_docdir}/%{name}/*
%{_datadir}/applications/gzdoom.desktop
%{_datadir}/icons/hicolor/256x256/apps/gzdoom.xpm
%{_datadir}/games/doom/*

%changelog
* Mon Aug 11 2025 corngoblin <wookie@cookies.com> - 4.14.2-1
- Updated to upstream version 4.14.2 (tag g4.14.2)
