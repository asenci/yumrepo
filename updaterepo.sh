#!/bin/bash

set -eo pipefail

if [ -z "${*}" ]; then
  find repo -maxdepth 1 -mindepth 1 -type d -print0 | xargs -0 "${0}"
  exit "${?}"
fi

for REPO in "${@}"; do
  createrepo --update "${REPO}"
done
