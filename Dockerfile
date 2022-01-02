FROM fedora:35

RUN dnf -y install --setopt=tsflags=nodocs \
  createrepo \
  git-core \
  rpm-build \
  rpmdevtools \
  rpmlint \
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
