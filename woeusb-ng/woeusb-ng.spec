Name:           woeusb-ng
Version:        0.2.10
Release:        1%{?dist}
Summary:        Tool to create a bootable Windows installer drive

License:        GPL-3.0-or-later
URL:            https://github.com/WoeUSB/WoeUSB-ng
Source0:        https://files.pythonhosted.org/packages/source/W/WoeUSB-ng/WoeUSB-ng-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-termcolor
BuildRequires:  python3-wxpython4
BuildRequires:  ImageMagick
BuildRequires:  potrace

Requires:       python3-termcolor
Requires:       python3-wxpython4
Requires:       xdg-utils
Requires:       p7zip

# Old woeusb package ships binaries with the same names,
# so this package conflicts with it
Conflicts:      woeusb

%description
WoeUSB-ng is a simple tool that enables you to create your own Windows installer
USB drive from an ISO image or a real DVD. This is a Python rewrite of the
original WoeUSB.

%prep
%autosetup -n WoeUSB-ng-%{version}
# Ensure Python shebangs are consistent
find . -type f -exec sed -i -e 's|/usr/bin/env python3|/usr/bin/python3|' {} \;

%build
%py3_build

%install
# Adjust install prefix
sed -i -e 's|/usr/local/bin/woeusbgui|%{buildroot}%{_bindir}/woeusbgui|' setup.py
%py3_install

# Generate SVG icon from bundled PNG
convert WoeUSB/data/woeusb-logo.png WoeUSB/data/woeusb.svg
install -Dm0644 WoeUSB/data/woeusb.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/woeusb.svg

# Install .desktop file
cat > %{buildroot}%{_datadir}/applications/woeusb-ng.desktop <<EOF
[Desktop Entry]
Name=WoeUSB-ng
Comment=Windows installation drive creator
Exec=woeusbgui
Icon=woeusb
Terminal=false
Type=Application
Categories=Utility;
EOF

%files
%doc README.md
%license LICENSE
%{_bindir}/woeusb
%{_bindir}/woeusbgui
%{_datadir}/applications/woeusb-ng.desktop
%{_datadir}/icons/hicolor/scalable/apps/woeusb.svg
%{python3_sitelib}/WoeUSB*
%{python3_sitelib}/WoeUSB_ng-*.egg-info

%changelog
* Fri Sep 26 2025 Your Name <you@example.com> - 0.2.10-1
- Initial Fedora package
