# Global settings
%global major_version 1
%global minor_version 1
%global micro_version 14
%global archive_name ZMusic

Name:           zmusic
Version:        %{major_version}.%{minor_version}.%{micro_version}
Release:        2%{?dist}
Summary:        ZMusic libraries and headers for GZDoom functionality
License:        GPLv3
Url:            http://zdoom.org
Source0:        https://github.com/coelckers/ZMusic/archive/%{version}.tar.gz

Provides:       zmusic = %{major_version}.%{minor_version}.%{micro_version}

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
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

%package        devel
Summary:        ZMusic development headers
Requires:       zmusic = %{version}-%{release}

%description    devel
This package contains the development headers required for building against
zmusic, typically for gzdoom installations.

%prep
%setup -q -n %{archive_name}-%{version}

%build
# Methodology used from zdoom forums
mkdir build
cd build
%cmake  -B builddir \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=%{_prefix} \
        -DCMAKE_INSTALL_LIBDIR=%{_lib} ..

%make_build %{?_smp_mflags} -C builddir

%install
rm -rf $RPM_BUILD_ROOT

cd build
%make_install -C builddir

%files
%defattr(-, root, root, -)
%doc licenses/*
%{_libdir}/*

%files devel
%defattr(-, root, root, -)
%{_includedir}/*

%changelog
* Fri Jan 03 2025 Louis Abel <tucklesepk@gmail.com> - 1.1.14-2
- Rebuild

* Sat Oct 12 2024 Louis Abel <tucklesepk@gmail.com> - 1.1.14-2
- Rebase to 1.1.14

* Thu Sep 21 2023 Louis Abel <tucklesepk@gmail.com> - 1.1.12-2
- Repair changelog date and rebuild zmusic

* Tue Apr 04 2023 Louis Abel <tucklesepk@gmail.com> - 1.1.12-1
- Rebase to 1.1.12

* Sat Nov 05 2022 Louis Abel <tucklesepk@gmail.com> - 1.1.11-1
- Rebase to 1.1.11

* Mon Jun 06 2022 Louis Abel <tucklesepk@gmail.com> - 1.1.9-1
- Rebase to 1.1.9

* Tue May 25 2021 Louis Abel <tucklesepk@gmail.com> - 1.1.8-1
- Fix requirements to use pkgconfig
- Rebase to 1.1.8

* Tue Mar 30 2021 Louis Abel <tucklesepk@gmail.com> - 1.1.6-3
- Rebase to 1.1.6

* Mon Oct 26 2020 Louis Abel <tucklesepk@gmail.com> - 1.1.3-2
- Build for Fedora 33
- Adapt to Fedora macro changes for out-of-source builds
- Fix provides

* Sun Sep 27 2020 Louis Abel <tucklesepk@gmail.com> - 1.1.3-1
- Rebase to 1.1.3
- lib and lib64 installs fixed

* Sun Jun 14 2020 Louis Abel <tucklesepk@gmail.com> - 1.1.0-1
- Initial zmusic build

