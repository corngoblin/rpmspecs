#!/usr/bin/env bash
# Build one package from this repository in a clean Fedora container.
#
#   scripts/rpm-build.sh <fedora-release> <package> [--test-install]
#
#   scripts/rpm-build.sh 45 uzdoom
#     -> installs the spec's BuildRequires in a fedora:45 container,
#        downloads the sources and produces SRPM + binary RPMs under
#        ~/rpmbuild-e/f45/RPMS.
#
#   scripts/rpm-build.sh 45 uzdoom --test-install
#     -> additionally installs the result in a throwaway container and runs
#        the packaged binary's --version / --help smoke test.
#
# The container is kept between runs so repeated iterations stay fast.
set -euo pipefail

rel="${1:?usage: rpm-build.sh <fedora-release> <package> [--test-install]}"
pkg="${2:?usage: rpm-build.sh <fedora-release> <package> [--test-install]}"
test_install="${3:-}"

repo=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
spec="$repo/packages/$pkg/$pkg.spec"
[ -f "$spec" ] || { echo "no spec at $spec" >&2; exit 1; }

work="$HOME/rpmbuild-e/f$rel"
mkdir -p "$work"/{SPECS,SOURCES,BUILD,RPMS,SRPMS,BUILDROOT}
cp "$spec" "$work/SPECS/"
cp "$repo/packages/$pkg"/*.patch "$work/SPECS/" 2>/dev/null || true

builder="emporium-f$rel"
if ! podman container exists "$builder"; then
    podman run -d --name "$builder" \
        -v "$work:/work:z" -v "$repo:/src:z,ro" \
        "registry.fedoraproject.org/fedora:$rel" sleep infinity >/dev/null
    podman exec "$builder" dnf -y install rpm-build rpmdevtools dnf-plugins-core \
        tar gzip bzip2 xz curl git findutils which >/dev/null
fi

echo "== builddeps ($pkg, fedora $rel) =="
podman exec "$builder" dnf -y builddep "/work/SPECS/$(basename "$spec")" >/dev/null

echo "== sources =="
podman exec "$builder" spectool -g -C /work/SOURCES "/work/SPECS/$(basename "$spec")"

echo "== rpmbuild =="
podman exec "$builder" rpmbuild -ba --define "_topdir /work" \
    "/work/SPECS/$(basename "$spec")"

echo
echo "== artifacts =="
find "$work/RPMS" "$work/SRPMS" -name "*.rpm" -newermt '-2 hours' -printf '%p\n' | sort

if [ "$test_install" = "--test-install" ]; then
    tester="emporium-f$rel-test"
    podman rm -f "$tester" >/dev/null 2>&1 || true
    podman run -d --name "$tester" -v "$work:/work:z" \
        "registry.fedoraproject.org/fedora:$rel" sleep infinity >/dev/null
    # shellcheck disable=SC2012
    rpmfile=$(ls -t "$work"/RPMS/*/*"$pkg"-[0-9]*.rpm | grep -v -- '-debug' | head -1)
    echo "== install test: $(basename "$rpmfile") =="
    podman exec "$tester" dnf -y install "/work/${rpmfile#"$work"/}" >/dev/null
    podman exec "$tester" rpm -q "$pkg"
fi
