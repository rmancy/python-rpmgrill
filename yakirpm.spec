%global commit placeholder
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name: yakirpm
Version: 0.1
Release: 1%{?dist}
Summary: YakiRPM is a python library for using rpmgrill

License: GPLv2+
URL: https://github.com/rmancy/YakiRPM
Source0:  https://github.com/rmancy/YakiRPM/archive/%{commit}/%{name}-%{version}.tar.gz
BuildRequires: python
BuildRequires: python-devel
BuildRequires: python-setuptools
BuildRequires: pytest

Requires: rpmgrill >= 0.26

%description
YakiRPM is a python library for doing local analysis of RPM packages via
rpmgrill. Please see the perl rpmgrill package for further details.

%prep
%setup -q


%build
CFLAGS="%{optflags}" %{__python2} setup.py build

%install
%{__python2}  setup.py install --skip-build --root %{buildroot}

%check
# We need to create seperate unit tests to be able
# to test them here
#python setup.py test

%files
%doc /usr/share/doc/yakirpm/
%{python2_sitelib}/yakirpm/
%{python2_sitelib}/yakirpm*.egg-info


%changelog

