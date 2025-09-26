Name:           woeusb-ng
Version:        0.2.10
Release:        1%{?dist}
Summary:        Bootable Windows USB creator for Linux

License:        GPL-3.0-or-later
URL:            https://github.com/WoeUSB/WoeUSB-ng
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3
Requires:       wxPython

%description
WoeUSB-ng is a simple tool that lets you create your own bootable Windows 
installation USB stick from an ISO image or a real DVD.

%prep
%autosetup -n WoeUSB-ng-%{version}

%build
%py3_build

%install
%py3_install

# Move non-Python data files out of site-packages into correct FHS dirs
mkdir -p %{buildroot}%{_datadir}/woeusb-ng
cp -pr %{buildroot}%{python3_sitelib}/WoeUSB/data %{buildroot}%{_datadir}/woeusb-ng/
rm -rf %{buildroot}%{python3_sitelib}/WoeUSB/data

# Translations → /usr/share/locale
mkdir -p %{buildroot}%{_datadir}/locale
cp -pr %{buildroot}%{python3_sitelib}/WoeUSB/locale/* %{buildroot}%{_datadir}/locale/
rm -rf %{buildroot}%{python3_sitelib}/WoeUSB/locale

%files
%license LICENSE
%doc README.md
%{_bindir}/woeusb
%{_bindir}/woeusbgui
%{python3_sitelib}/WoeUSB
%{python3_sitelib}/WoeUSB_ng-*.egg-info
%{_datadir}/woeusb-ng
%{_datadir}/locale/*/LC_MESSAGES/woeusb.*

%changelog
* Fri Sep 26 2025 Your Name <you@example.com> - 0.2.10-1
- Initial COPR package
