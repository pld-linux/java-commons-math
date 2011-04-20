# TODO
# - target jar depends on "tests", meaning not possible to build jar without
#   tests passing
#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_without	tests		# don't build and run tests

%define		srcname		commons-math
%include	/usr/lib/rpm/macros.java
Summary:	Java library of lightweight mathematics and statistics components
Name:		java-%{srcname}
Version:	2.2
Release:	0.1
License:	ASL 1.1 and ASL 2.0 and BSD
Group:		Development/Libraries
URL:		http://commons.apache.org/math/
Source0:	http://www.apache.org/dist/commons/math/source/%{srcname}-%{version}-src.tar.gz
# Source0-md5:	6261d7991154c992477b32b8f3bea18b
BuildRequires:	jdk >= 1.6
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.555
%{?with_tests:BuildRequires:	java-junit >= 4.3}
%if %(locale -a | grep -q '^en_US$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Commons Math is a library of lightweight, self-contained mathematics
and statistics components addressing the most common problems not
available in the Java programming language or Commons Lang.

%package javadoc
Summary:	Javadoc for commons-math
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
This package contains the API documentation for commons-math.

%prep
%setup -q -n commons-math-%{version}-src

%build
# source code not US-ASCII
export LC_ALL=en_US

%if %{with tests}
junit=$(find-jar junit)
%endif

%ant \
	-Dskip.download=1 \
	-Djunit.jar=$junit \
	jar %{?with_javadoc:javadoc}

%install
rm -rf $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt

%files javadoc
