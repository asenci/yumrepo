Name:     readsb
Version:  4.4.0.1
Release:  1%{?dist}
Summary:  Mode-S/ADSB/TIS decoder for RTLSDR, BladeRF, Modes-Beast and GNS5894 devices
License:  GPLv3
URL:      https://github.com/adsbxchange/readsb/
Source0:  https://github.com/asenci/readsb/archive/v%{version}.tar.gz

Source1:  readsb.sysconfig
Source2:  readsb.service

Patch0:   Makefile.patch

BuildRequires: gcc make systemd-rpm-macros
BuildRequires: libusb1-devel
BuildRequires: ncurses-devel
BuildRequires: rtl-sdr-devel
BuildRequires: zlib-devel

%{?systemd_ordering}

%description
Readsb is a Mode-S/ADSB/TIS decoder for RTLSDR, BladeRF, Modes-Beast
and GNS5894 devices. As a former fork of dump1090-fa it is using that
code base but development will continue as a standalone project with
new name. Readsb can co-exist on the same host system with dump1090-fa,
it doesn't use or modify its resources. However both programs will not
share a receiver device at the same time and in parallel.


%prep
%setup -q -n readsb-%{version}
%patch0 -p1

%build
READSB_VERSION="%{version}"; export READSB_VERSION
%set_build_flags
%make_build RTLSDR=yes HAVE_BIASTEE=yes


%install
install -Dpm 0755 readsb %{buildroot}%{_bindir}/readsb
install -Dpm 0755 viewadsb %{buildroot}%{_bindir}/viewadsb

install -Dpm 0644 debian/readsb.1 %{buildroot}%{_mandir}/man1/readsb.1
install -Dpm 0644 debian/viewadsb.1 %{buildroot}%{_mandir}/man1/viewadsb.1

install -Dpm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/readsb
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_unitdir}/readsb.service

%pre
getent passwd readsb >/dev/null 2>&1 || useradd \
  --comment 'Mode-S/ADSB/TIS decoder' \
  --groups rtlsdr \
  --system \
  --home-dir / \
  --shell /sbin/nologin \
  readsb

%post
%systemd_post readsb.service

%preun
%systemd_preun readsb.service

%postun
%systemd_postun_with_restart readsb.service


%files
%license LICENSE

%doc README*.md
%doc debian/README.librtlsdr

%config(noreplace) %{_sysconfdir}/sysconfig/readsb

%{_bindir}/readsb
%{_bindir}/viewadsb
%{_mandir}
%{_unitdir}/readsb.service

%changelog
* Sun Feb 27 2022 Andre Sencioles <asenci@gmail.com> - 4.4.0.1-1
- Initial release
