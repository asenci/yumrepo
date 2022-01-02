#!/bin/bash

set -eo pipefail

if [ -z "${*}" ]; then
  find docs -maxdepth 1 -mindepth 1 -type d -print0 | xargs -0r "${0}"
  exit
fi

for REPO in "${@}"; do
  createrepo --update "${REPO}"
done
