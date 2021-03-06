%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}
Name:     tcl-tcllauncher
Version:  1.10
Release:  3%{?dist}
Summary:  Launcher program for Tcl applications
License:  BSD 3-Clause License
URL:      https://github.com/flightaware/tcllauncher
Source0:  https://github.com/flightaware/tcllauncher/archive/v%{version}.tar.gz

Patch0: tcllauncher-1.10.patch

Provides: tcllauncher = %{version}

BuildRequires: autoconf tcl-devel

Requires: tclx

%description
tcllauncher is a way to have Tcl programs run out of /usr/local/bin under their own name, be installed in one place with their support files, and provides commands to facilitate server-oriented application execution.


%prep
%setup -qn tcllauncher-%{version}
%patch0 -p1

%build
autoconf
%configure --libdir=%{tcl_sitearch} --with-tcl=%{tcl_sitearch}
%make_build

%install
%make_install


%files
%license LICENSE
%license license.terms

%doc README.md

%{_bindir}/tcllauncher
%{tcl_sitearch}
%{_mandir}


%changelog
* Mon Jan 31 2022 Andre Sencioles <asenci@gmail.com> - 1.10-3
- Add package alias

* Mon Jan 31 2022 Andre Sencioles <asenci@gmail.com> - 1.10-2
- Fix tcllauncher TCL library search path

* Sat Jan 29 2022 Andre Sencioles <asenci@gmail.com> - 1.10-1
- Initial release
