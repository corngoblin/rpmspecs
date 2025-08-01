Name:           duckstation
Version:        0.1.9226
Release:        1%{?dist}
Summary:        PlayStation 1 emulator

License:        CC-BY-NC-ND-4.0
URL:            https://github.com/stenzek/duckstation
Source0:        https://github.com/stenzek/duckstation/archive/refs/tags/v0.1-9226.tar.gz#/duckstation-0.1.9226.tar.gz

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
DuckStation is a PlayStation 1 emulator that focuses on speed, accuracy, and maintainability.

%prep
%autosetup -n duckstation-v0.1-9226

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
* Fri Aug 01 2025 MonkeyGold <your@email.com> - 0.1.9226-1
- Initial automated build of DuckStation from GitHub tag v0.1-9226
