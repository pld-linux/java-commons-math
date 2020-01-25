# TODO
# - tests fail. a lot
# - junit needed for compile target
#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_with	tests		# don't build and run tests

%define		srcname		commons-math
Summary:	Java library of lightweight mathematics and statistics components
Name:		java-%{srcname}
Version:	2.2
Release:	1
License:	ASL 1.1 and ASL 2.0 and BSD
Group:		Development/Libraries
URL:		http://commons.apache.org/math/
Source0:	http://www.apache.org/dist/commons/math/source/%{srcname}-%{version}-src.tar.gz
# Source0-md5:	6261d7991154c992477b32b8f3bea18b
Patch0:		notest.patch
BuildRequires:	java-junit >= 4.3
BuildRequires:	jdk >= 1.6
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.555
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
%patch0 -p1

%build
# source code not US-ASCII
export LC_ALL=en_US

%ant \
	-Dskip.download=1 \
	jar %{?with_javadoc:javadoc}

%if %{with tests}
junit=$(find-jar junit)
%ant \
	-Djunit.jar=$junit
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

# jars
cp -p target/%{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a target/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt
%{_javadir}/%{srcname}.jar
%{_javadir}/%{srcname}-%{version}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
