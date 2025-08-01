Name:           duckstation
Version:        lastest
Release:        1%{?dist}
Summary:        PlayStation 1 emulator

License:        CC-BY-NC-ND-4.0
URL:            https://github.com/stenzek/duckstation
Source0:        https://github.com/stenzek/duckstation/archive/refs/tags/v%{version}.tar.gz#/duckstation-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qttools-devel
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libGL-devel
BuildRequires:  libX11-devel

%description
DuckStation is a PlayStation 1 emulator that aims to be accurate and user-friendly.

%prep
%autosetup -n duckstation-%{version}

%build
mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=%{_prefix}
make %{?_smp_mflags}

%install
cd build
make install DESTDIR=%{buildroot}

%files
%{_bindir}/duckstation
%{_datadir}/duckstation/
%{_libdir}/duckstation/
%license LICENSE

%changelog
* Thu Jul 31 2025 Your Name <youremail@example.com> - 0.1.0-1
- Initial package
