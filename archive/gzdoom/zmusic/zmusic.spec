%global forgeurl https://github.com/coelckers/ZMusic
%global tag %{version}
%forgemeta

Name:           zmusic
Version:        1.1.14
Release:        2%{?dist}
Summary:        ZMusic libraries and headers for GZDoom functionality
License:        GPLv3
URL:            %{forgeurl}
Source0:        %{forgesource}

Provides:       zmusic = %{version}

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  cmake
BuildRequires:  tar
BuildRequires:  git
BuildRequires:  nasm
BuildRequires:  glew-devel

# pkgconfig
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(fluidsynth)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(sdl)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(libgme)
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(libmpg123)

BuildRequires:  timidity++
BuildRequires:  pkgconfig(wildmidi)

%description
ZDoom is a family of enhanced ports (modifications) of the Doom engine for
running on modern operating systems. It runs on Windows, Linux, and OS X, and
adds new features not found in the games as originally published by id Software.

This package provides the necessary zmusic libraries necessary for gzdoom to
function.

%package devel
Summary:        ZMusic development headers
Requires:       zmusic = %{version}-%{release}

%description devel
This package contains the development headers required for building against
zmusic, typically for gzdoom installations.

%prep
%forgeautosetup

%build
%cmake -B builddir \
       -DCMAKE_BUILD_TYPE=Release \
       -DCMAKE_INSTALL_PREFIX=%{_prefix} \
       -DCMAKE_INSTALL_LIBDIR=%{_lib}

%make_build -C builddir

%install
rm -rf %{buildroot}
%make_install -C builddir

%files
%defattr(-, root, root, -)
%doc licenses/*
%{_libdir}/*

%files devel
%defattr(-, root, root, -)
%{_includedir}/*

%changelog
* Mon Aug 11 2025 corngoblin <wookie@cookies.com> - 4.14.2-1
- Updated to latest upstream release
