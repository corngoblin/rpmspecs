Name:           woeusb-ng
Version:        0.2.12
Release:        1%{?dist}
Summary:        Create a Windows USB stick installer from a real Windows DVD or image

License:        GPLv3+
URL:            https://github.com/WoeUSB/WoeUSB-ng
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Patch out upstream’s hardcoded /usr/local install hacks in setup.py
Patch0:         %{name}-setup-no-postinstall.patch

BuildArch:      noarch

# Build system
BuildRequires:  python3-devel
BuildRequires:  python3-pyproject-rpm-macros
BuildRequires:  fdupes
BuildRequires:  desktop-file-utils
BuildRequires:  polkit

# Runtime deps
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
WoeUSB-ng is a Linux program to create a Windows USB stick installer from
a real Windows DVD or disk image.

It provides:
- woeusb: command-line utility
- woeusbgui: graphical utility

Supported images:
- Windows Vista, Windows 7, Windows 8.x, Windows 10
- All editions, languages, and Windows PE

Supported boot modes:
- Legacy/MBR-style boot
- UEFI boot for Windows 7+ (FAT target required)

%prep
%autosetup -p1 -n WoeUSB-ng-%{version}
# fix shebangs
sed -i '1s|/usr/bin/env python3|/usr/bin/python3|' WoeUSB/{core.py,gui.py,list_devices.py,woeusb,woeusbgui}
# fix desktop icon name
sed -i 's|^Icon=.*|Icon=woeusb-ng|' miscellaneous/WoeUSB-ng.desktop

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files WoeUSB

# Install icon (256x256 png)
install -Dm644 WoeUSB/data/woeusb-logo.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/woeusb-ng.png

# Install desktop entry
install -Dm644 miscellaneous/WoeUSB-ng.desktop \
  %{buildroot}%{_datadir}/applications/WoeUSB-ng.desktop

# Install polkit policy
install -Dm644 miscellaneous/com.github.woeusb.woeusb-ng.policy \
  %{buildroot}%{_datadir}/polkit-1/actions/com.github.woeusb.woeusb-ng.policy

%fdupes %{buildroot}%{python3_sitelib}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/WoeUSB-ng.desktop

%files -f %{pyproject_files}
%doc README.md
%license COPYING
%{_bindir}/woeusb
%{_bindir}/woeusbgui
%{_datadir}/applications/WoeUSB-ng.desktop
%{_datadir}/icons/hicolor/256x256/apps/woeusb-ng.png
%{_datadir}/polkit-1/actions/com.github.woeusb.woeusb-ng.policy

%changelog
* Mon Aug 18 2025 Monkeygold - 0.2.12-1

