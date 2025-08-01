Name:           duckstation
Version:        0.1.9226
Release:        1%{?dist}
Summary:        Fast PlayStation 1 emulator

License:        CC-BY-NC-ND-4.0
URL:            https://github.com/stenzek/duckstation

# Tag and project directory
%global tag_name        v0.1-9226
# Don't hardcode project_dir here, detect dynamically in %prep

%global discord_rpc_ver cc59d26d1d628fbd6527aac0ac1d6301f4978b92

Source0:        https://github.com/stenzek/duckstation/archive/refs/tags/%{tag_name}.tar.gz
Source1:        https://github.com/stenzek/discord-rpc/archive/%{discord_rpc_ver}.tar.gz

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
# ... [other BuildRequires as in your spec] ...

ExclusiveArch:  x86_64 aarch64

%description
DuckStation is a fast and accurate PlayStation 1 emulator, focused on speed, playability, and long‑term maintainability.

%prep
# Extract the main source archive quietly
%setup -q

# Now find the extracted directory dynamically:
project_dir=$(tar tzf %{SOURCE0} | head -1 | cut -f1 -d"/")

# Extract DiscordRPC source
tar -xf %{SOURCE1}
mv discord-rpc-%{discord_rpc_ver} discord-rpc

# Change into the project directory to prepare for build
cd "$project_dir" || exit 1

# Export project_dir for later usage
echo "export PROJECT_DIR=$project_dir" > %{_builddir}/project_dir.env

%build
# Load project_dir from prep stage
. %{_builddir}/project_dir.env

# Build DiscordRPC first
pushd "$PROJECT_DIR"/discord-rpc
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF -DCMAKE_POSITION_INDEPENDENT_CODE=ON
cmake --build . --target discord-rpc
popd

# Build DuckStation
%cmake -B build -G Ninja \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DUSE_QT6=ON \
  -DDUCKSTATION_QT_UI=ON \
  -DDISCORDRPC_SUPPORT=ON \
  -DDiscordRPC_INCLUDE_DIR=%{_builddir}/$PROJECT_DIR/discord-rpc/include \
  -DDiscordRPC_LIBRARY=%{_builddir}/$PROJECT_DIR/discord-rpc/build/libdiscord-rpc.a \
  -DDiscordRPC_FOUND=TRUE \
  "$PROJECT_DIR"

%ninja_build -C build

%install
%ninja_install -C build

desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/org.duckstation.DuckStation.desktop || :

install -Dm644 %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/org.duckstation.DuckStation.png \
  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/org.duckstation.DuckStation.png || :

%files
%license LICENSE
%doc README.md
%{_bindir}/duckstation-qt
%{_datadir}/applications/org.duckstation.DuckStation.desktop
%{_datadir}/icons/hicolor/128x128/apps/org.duckstation.DuckStation.png

%changelog
* Thu Jul 31 2025 Monkegold <o53cbexp0@mozmail.com> - 0.1.9226-1
- Updated to tag v0.1-9226
- Switched to SDL3
- Enabled DiscordRPC support with embedded build
- Ensured compatibility with Fedora 42 and Rawhide
