#!/bin/bash

set -eo pipefail

if [ -z "${*}" ]; then
  find . -iname '*.spec' -print0 | xargs -0r "${0}"
  exit
fi

for SPEC in "${@}"; do
  BASEPATH=$(dirname $(dirname "${SPEC}"))

  yum-builddep -y "${SPEC}"

  spectool -g -C "${BASEPATH}/SOURCES" "${SPEC}"

  rpmbuild -ba --nocheck \
    --define "_topdir ${PWD}/${BASEPATH}" \
    --define "_rpmdir ${PWD}/docs/%{_build_arch}/packages" \
    --define "_srcrpmdir ${PWD}/docs/Source/packages" \
    --define "_build_name_fmt %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm" \
    "${SPEC}"
done
