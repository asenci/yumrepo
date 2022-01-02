#!/bin/bash

set -eo pipefail

if [ -z "${*}" ]; then
  find . -iname '*.spec' -print0 | xargs -0r "${0}"
  exit
fi

for SPEC in "${@}"; do
  RPMLINTRC=$(dirname $(dirname "${SPEC}"))/.rpmlintrc
  if [ -f "${RPMLINTRC}" ]; then
    RPMLINTARGS+=("--rpmlintrc" "${RPMLINTRC}")
  fi

  rpmlint "${RPMLINTARGS[@]}" "${SPEC}"
done
