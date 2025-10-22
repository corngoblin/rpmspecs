%global forgeurl https://github.com/ghostty-org/ghostty
%global commit 9dc2e5978f6ee69f4d784b61865589b502c4012d
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%forgemeta

Name:           ghostty-git
Version:        1.2.3
Release:        %autorelease -s git%{shortcommit}
Summary:        Fast, feature-rich, and cross-platform terminal emulator that uses platform-native UI and GPU acceleration
License:        MIT
URL:            %{forgeurl}
Source:         %{forgesource}

BuildRequires: coreutils
BuildRequires: blueprint-compiler
BuildRequires: fontconfig-devel
BuildRequires: freetype-devel
BuildRequires: glib2-devel
BuildRequires: glslang-devel
BuildRequires: gtk4-devel
BuildRequires: gtk4-layer-shell-devel
BuildRequires: harfbuzz-devel
BuildRequires: libadwaita-devel
BuildRequires: libpng-devel
BuildRequires: libxml2-devel
BuildRequires: oniguruma-devel
BuildRequires: pandoc-cli
BuildRequires: pixman-devel
BuildRequires: pkg-config
BuildRequires: simdutf-devel
BuildRequires: wayland-protocols-devel
BuildRequires: zig >= 0.14.0
BuildRequires: zlib-ng-devel

Requires: fontconfig
Requires: freetype
Requires: glib2
Requires: gtk4
Requires: harfbuzz
Requires: libadwaita
Requires: libpng
Requires: oniguruma
Requires: pixman
Requires: zlib-ng
Requires: ncurses-term

%description
%{summary}.

%prep
%forgeautosetup

%build
export ZIG_GLOBAL_CACHE_DIR="$(mktemp --directory)"
./nix/build-support/fetch-zig-cache.sh
DESTDIR=%{buildroot} zig build \
    --summary all \
    --prefix "%{_prefix}" \
    --system "${ZIG_GLOBAL_CACHE_DIR}/p" \
    -Dversion-string=%{version}-%{release} \
    -Doptimize=ReleaseFast \
    -Dcpu=baseline \
    -Dpie=true \
    -Demit-docs
find "%{buildroot}/usr/share/locale" -type f -name "com.mitchellh.ghostty.mo" | sed "s|%{buildroot}||" > message_catalogs.txt

# Remove terminfo files that conflict with ncurses-term
rm -f %{buildroot}%{_datadir}/terminfo/g/ghostty

%files -f message_catalogs.txt
%license LICENSE
%{_bindir}/ghostty
%{_prefix}/lib/systemd/user/app-com.mitchellh.ghostty.service
%{_prefix}/share/dbus-1/services/com.mitchellh.ghostty.service
%{_prefix}/share/applications/com.mitchellh.ghostty.desktop
%{_prefix}/share/bash-completion/completions/ghostty.bash
%{_prefix}/share/bat/syntaxes/ghostty.sublime-syntax
%{_prefix}/share/fish/vendor_completions.d/ghostty.fish
%{_prefix}/share/ghostty
%{_prefix}/share/icons/hicolor/1024x1024/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/128x128/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/128x128@2/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/16x16/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/16x16@2/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/256x256/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/256x256@2/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/32x32/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/32x32@2/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/512x512/apps/com.mitchellh.ghostty.png
%{_prefix}/share/kio/servicemenus/com.mitchellh.ghostty.desktop
%{_prefix}/share/man/man1/ghostty.1
%{_prefix}/share/man/man5/ghostty.5
%{_prefix}/share/metainfo/com.mitchellh.ghostty.metainfo.xml
%{_prefix}/share/nautilus-python/extensions/ghostty.py
%{_prefix}/share/nvim/site/compiler/ghostty.vim
%{_prefix}/share/nvim/site/ftdetect/ghostty.vim
%{_prefix}/share/nvim/site/ftplugin/ghostty.vim
%{_prefix}/share/nvim/site/syntax/ghostty.vim
%{_prefix}/share/terminfo/x/xterm-ghostty
%{_prefix}/share/vim/vimfiles/compiler/ghostty.vim
%{_prefix}/share/vim/vimfiles/ftdetect/ghostty.vim
%{_prefix}/share/vim/vimfiles/ftplugin/ghostty.vim
%{_prefix}/share/vim/vimfiles/syntax/ghostty.vim
%{_prefix}/share/zsh/site-functions/_ghostty
%{_includedir}/ghostty/vt.h
/usr/lib/libghostty-vt.so
%{_datadir}/pkgconfig/libghostty-vt.p

%changelog
%autochangelog
