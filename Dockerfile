FROM fedora:38

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
  https://asenci.github.io/yumrepo/x86_64/packages/asenci-release-1-1.noarch.rpm \
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
