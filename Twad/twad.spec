%global goipath         github.com/zmnpl/twad
%global commit          v0.30.0
%global gobuildmode     -o twad

Name: twad
Version: 0.30.0
Release: 1%{?dist}
Summary: A DOOM WAD manager
License: GPLv3+
URL: https://github.com/zmnpl/twad
Source0: https://github.com/zmnpl/twad/archive/v%{version}/twad-%{version}.tar.gz

BuildRequires: golang

%description
Twad is a doom wad manager that lets you set up a multitude of WAD file combinations, store and launch them with a couple of key strokes. It is light weight and fast to use. If your are living in the termninal you'll feel right at home. 

%prep
%autosetup -n twad-%{version}

%build
go build -o twad .

%install
install -m 755 -d %{buildroot}%{_bindir}
install -m 755 twad %{buildroot}%{_bindir}/twad

%files
%license COPYING
%{_bindir}/twad
