Name:           woeusb-ng
Version:        0.2.12
Release:        1%{?dist}
Summary:        Create a Windows USB stick installer from a real Windows DVD or image
License:        GPLv3+
URL:            https://github.com/WoeUSB/WoeUSB-ng
Source0:        https://github.com/WoeUSB/WoeUSB-ng/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  polkit
BuildRequires:  python3-setuptools
BuildRequires:  python3-distutils-extra
BuildRequires:  fdupes
Requires:       bash
Requires:       dosfstools
Requires:       gawk
Requires:       grep
Requires:       grub2-pc-modules
Requires:       ntfs-3g
Requires:       parted
Requires:       wget
Requires:       wimlib
Requires:       wimlib-utils
Requires:       polkit
Requires:       python3-wxpython4

%description
A Linux program to create a Windows USB stick installer from a real Windows DVD or image.

This package contains two programs:
- woeusb: A command-line utility that enables you to create your own bootable
          Windows installation USB storage device
- woeusbgui: Graphical frontend for woeusb

Supported images: Windows Vista, 7, 8.x, 10, 11.

Supported boot modes:
- Legacy BIOS (MBR)
- UEFI (Windows 7+)

%prep
%autosetup -n WoeUSB-ng-%{version}

%build
%py3_build

%install
%py3_install

# Install icon and desktop integration
install -D -m644 WoeUSB/data/woeusb-logo.png \
    %{buildroot}%{_datadir}/pixmaps/%{name}.png

install -D -m644 miscellaneous/WoeUSB-ng.desktop \
    %{buildroot}%{_datadir}/applications/WoeUSB-ng.desktop

install -D -m644 miscellaneous/com.github.woeusb.%{name}.policy \
    %{buildroot}%{_datadir}/polkit-1/actions/com.github.woeusb.%{name}.policy

%fdupes %{buildroot}%{python3_sitelib}

%files
%license COPYING
%doc README.md
%{_bindir}/woeusb
%{_bindir}/woeusbgui
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/WoeUSB-ng.desktop
%{_datadir}/polkit-1/actions/com.github.woeusb.%{name}.policy
%{python3_sitelib}/WoeUSB*

%changelog
* Mon Aug 18 2025 Monkeygold 0.2.12-1
- Initial build for Fedora COPR
