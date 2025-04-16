%global debug_package %{nil}
%undefine _package_note_file

Name: starship
Version: 1.22.1
Release: 2%{?dist}
Summary: â˜„ðŸŒŒï¸� The minimal, blazing-fast, and infinitely customizable prompt for any shell!

License: ISC
URL: https://github.com/starship/starship
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1: starship.toml
Source2: nobara_profile_starship.sh

BuildRequires: cargo >= 1.74
BuildRequires: cmake3
BuildRequires: gcc
BuildRequires: rust >= 1.74

BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(zlib)
Requires:      nerd-fonts

%description
The minimal, blazing-fast, and infinitely customizable prompt for any shell!

  - Fast: it's fast â€“ really really fast! ðŸš€
  - Customizable: configure every aspect of your prompt.
  - Universal: works on any shell, on any operating system.
  - Intelligent: shows relevant information at a glance.
  - Feature rich: support for all your favorite tools.
  - Easy: quick to install â€“ start using it in minutes.


%prep
%autosetup


%install
export CARGO_PROFILE_RELEASE_BUILD_OVERRIDE_OPT_LEVEL=3
export CMAKE=cmake3
RUSTFLAGS='-C strip=symbols' cargo install --root=%{buildroot}%{_prefix} --path=.
rm -f %{buildroot}%{_prefix}/.crates.toml \
    %{buildroot}%{_prefix}/.crates2.json
mkdir -p %{buildroot}%{_datadir}/%{name}/
cp %{SOURCE1} %{buildroot}%{_datadir}/%{name}/

mkdir -p %{buildroot}/etc/profile.d
cp %{SOURCE2} %{buildroot}/etc/profile.d/


%files
%license LICENSE
%doc README.md CONTRIBUTING.md
%{_bindir}/%{name}
%{_datadir}/%{name}/starship.toml

