Name:           woeusb-ng
Version:        0.2.10
Release:        1%{?dist}
Summary:        A tool to create bootable Windows USB sticks

License:        GPL-3.0-or-later
URL:            https://github.com/WoeUSB/WoeUSB-ng
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  gcc
BuildRequires:  make
Requires:       python3
Requires:       util-linux
Requires:       parted
Requires:       grub2-efi-x64

%description
WoeUSB-ng is a Linux tool to create bootable USB sticks for Windows.

%prep
%autosetup -n WoeUSB-ng-%{version}

%build
export CXX
CFLAGS='-O2 -flto=auto -ffat-lto-objects -fexceptions -g -grecord-gcc-switches -pipe -Wall -Werror=format-security \
-Wp,-U_FORTIFY_SOURCE,-D_FORTIFY_SOURCE=3 -Wp,-D_GLIBCXX_ASSERTIONS -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 \
-fstack-protector-strong -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -m64 -march=x86-64 -mtune=generic \
-fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection -mtls-dialect=gnu2 -fno-omit-frame-pointer \
-mno-omit-leaf-frame-pointer'
LDFLAGS='-Wl,-z,relro -Wl,--as-needed -Wl,-z,pack-relative-relocs -Wl,-z,now -specs=/usr/lib/rpm/redhat/redhat-hardened-ld \
-specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -Wl,--build-id=sha1 -specs=/usr/lib/rpm/redhat/redhat-package-notes'

%install
rm -rf %{buildroot}
python3 setup.py install -O1 --skip-build --root %{buildroot} --prefix %{_prefix}

# Move data to /usr/share/woeusb-ng
mkdir -p %{buildroot}%{_datadir}/woeusb-ng
cp -pr %{buildroot}%{_libdir}/python3.%{python3_version}/site-packages/WoeUSB/data %{buildroot}%{_datadir}/woeusb-ng/
rm -rf %{buildroot}%{_libdir}/python3.%{python3_version}/site-packages/WoeUSB/data

# Move locales to /usr/share/locale
mkdir -p %{buildroot}%{_localstatedir}/locale
cp -pr %{buildroot}%{_libdir}/python3.%{python3_version}/site-packages/WoeUSB/locale/* %{buildroot}%{_localstatedir}/locale/
rm -rf %{buildroot}%{_libdir}/python3.%{python3_version}/site-packages/WoeUSB/locale

%files
%license COPYING
%doc README.md
%{_bindir}/woeusb
%{_bindir}/woeusbgui
%{_datadir}/woeusb-ng
%{_localstatedir}/locale

%changelog
* Thu Sep 26 2025 Your Name <you@example.com> - 0.2.10-1
- Initial Fedora 42 build
