%global forgeurl https://github.com/Stunkymonkey/nautilus-open-any-terminal
%global version 0.6.3
%global commit b4c9372cbe98682a297a695f6a1bc752fd3f864964b
%global date 20250918
%global source_date_epoch_from_changelog 0
%forgemeta


Name:           nautilus-open-any-terminal
Version:        %{forgeversion}
Release:        %{autorelease}
Summary:        Context-menu entry for opening other terminal in nautilus
License:        GPLv3
URL:            https://github.com/Stunkymonkey/nautilus-open-any-terminal

Source:        %{forgesource}

BuildArch:      noarch

BuildRequires:  gettext
BuildRequires:  make

Requires:       nautilus-python
Requires:       glib2


%description
An extension for nautilus, which adds an context-entry for opening other terminal emulators than gnome-terminal.

%prep
%forgesetup

%build
%make_build

%install
export DESTDIR="%{buildroot}"
make install-nautilus

%post
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files
%license LICENSE
%doc README.md
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/locale/*/LC_MESSAGES/*
%{_datadir}/nautilus-python/extensions/*

%changelog
%autochangelog 
