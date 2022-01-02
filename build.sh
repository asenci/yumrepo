#!/bin/bash

set -eo pipefail

if [ -z "${*}" ]; then
  find . -iname '*.spec' -print0 | xargs -0 "${0}"
  exit "${?}"
fi

for SPEC in "${@}"; do
  BASEPATH=$(dirname $(dirname "${SPEC}"))

  yum-builddep -y "${SPEC}"

  PARSEDSPEC=$(mktemp)

  rpmspec -P "${SPEC}" > "${PARSEDSPEC}"

  spectool -g -C "${BASEPATH}/SOURCES" "${PARSEDSPEC}"

  rpmbuild -ba --nocheck \
    --define "_topdir ${PWD}/${BASEPATH}" \
    --define "_rpmdir ${PWD}/repo/%{_build_arch}/packages" \
    --define "_srcrpmdir ${PWD}/repo/Source/packages" \
    --define "_build_name_fmt %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm" \
    "${SPEC}"
done
