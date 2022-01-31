Name:     mlat-client
Version:  0.2.12
Release:  1%{?dist}
Summary:  Mode S multilateration client
License:  GPLv3
URL:      https://github.com/mutability/mlat-client
Source0:  https://github.com/mutability/mlat-client/archive/v%{version}.tar.gz

BuildRequires:  python3-devel python3-wheel

%py_provides python3-mlat-client

%generate_buildrequires
%pyproject_buildrequires

%description
This is a client that selectively forwards Mode S messages to a server that resolves the transmitter position by multilateration of the same message received by multiple clients.

There is also support for running in a mode used to feed multilateration information to FlightAware via piaware. In this mode, the client is started automatically by piaware.


%prep
%setup -qn mlat-client-%{version}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files _modes flightaware mlat


%files -f %{pyproject_files}
%license COPYING

%doc README.md

%{_bindir}/mlat-client
%{_bindir}/fa-mlat-client


%changelog
* Mon Jan 31 2022 Andre Sencioles <asenci@gmail.com> - 0.2.12-1
- Initial release
