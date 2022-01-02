FROM fedora:35

RUN dnf -y install --setopt=tsflags=nodocs \
  cmake \
  cmake-rpm-macros \
  createrepo \
  gcc-c++ \
  git-core \
  rpm-build \
  rpmdevtools \
  rpmlint \
  systemd-rpm-macros \
  yum-utils \
  && dnf -y clean all \
  && mv /etc/adjtime.rpmnew /etc/adjtime \
  && rm -rf \
    /etc/nsswitch.conf.bak \
    /var/cache/dnf \
    /var/cache/ldconfig \
    /var/lib/dnf/repos \
    /var/log/dnf.* \
    /var/log/hawkey.log \
    /var/log/lastlog
