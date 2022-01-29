Name:     fr24feed
Summary:  FlightRadar24 data feeder
License:  GPLv3
URL:      https://www.flightradar24.com/share-your-data

%define upstream_version 1.0.25
%define upstream_release 3
Version:  %{upstream_version}_%{upstream_release}
Release:  2%{?dist}
Source0:  https://repo-feed.flightradar24.com/linux_x86_64_binaries/fr24feed_%{upstream_version}-%{upstream_release}_amd64.tgz
Source1:  fr24feed-status
Source2:  fr24feed.service

%{?systemd_ordering}


%description
Flightradar24 operates the world's largest network of ADS-B/Mode S receivers. This network, together with government air traffic control and other data sources, is how Flightradar24 is able to track aircraft around the globe.
You can help us increase the flight tracking coverage in your area by uploading data from your ADS-B receiver.


%prep
%setup -q -n fr24feed_amd64


%install
install -Dpm 0755 fr24feed %{buildroot}%{_bindir}/fr24feed
install -Dpm 0755 %{SOURCE1} %{buildroot}%{_bindir}/fr24feed-status
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_unitdir}/fr24feed.service


%pre
getent passwd fr24feed >/dev/null 2>&1 || useradd \
  --comment 'FlightRadar24 data feeder' \
  --system \
  --home-dir / \
  --shell /sbin/nologin \
  fr24feed

%post
%systemd_post fr24feed.service

%preun
%systemd_preun fr24feed.service

%postun
%systemd_postun_with_restart fr24feed.service


%files
%license licences/*
%{_bindir}/fr24feed
%{_bindir}/fr24feed-status
%{_unitdir}/fr24feed.service


%changelog
* Mon Jan 03 2022 Andre Sencioles <asenci@gmail.com> - 1.0.25_3-2
- Add status script
- Create fr24feed user during installation

* Mon Jan 03 2022 Andre Sencioles <asenci@gmail.com> - 1.0.25_3-1
- Initial release
