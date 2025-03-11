#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_with	tests	# unit tests (fapi tests fail)

%define		module	template
Summary:	TPM 2.0 TSS Bindings for Python
Summary(pl.UTF-8):	Wiązania TPM 2.0 TSS dla Pythona
Name:		python3-tpm2-pytss
Version:	2.1.0
Release:	3
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/tpm2-pytss/
Source0:	https://files.pythonhosted.org/packages/source/t/tpm2-pytss/tpm2-pytss-%{version}.tar.gz
# Source0-md5:	a629a192cd5a42b8d1e7ffab391de231
URL:		https://github.com/tpm2-software/tpm2-pytss
BuildRequires:	python3-asn1crypto
BuildRequires:	python3-cffi >= 1.0.0
BuildRequires:	python3-cryptography >= 3.0
BuildRequires:	python3-devel >= 1:3.7
BuildRequires:	python3-packaging
BuildRequires:	python3-pkgconfig
BuildRequires:	python3-pycparser
BuildRequires:	python3-setuptools >= 1:44
BuildRequires:	python3-setuptools_scm >= 3.4.3
BuildRequires:	python3-toml
%if %{with tests}
# or swtpm
BuildRequires:	ibmswtpm2
BuildRequires:	python3-PyYAML
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
# 3.3/4.0 when available in PLD
BuildRequires:	tpm2-tss-devel >= 2.4
%if %{with doc}
BuildRequires:	python3-myst_parser
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TPM2 TSS Python bindings for Enhanced System API (ESYS), Feature API
(FAPI), Marshaling (MU), TCTI Loader (TCTILdr) and RC Decoding
(rcdecode) libraries. It also contains utility methods for wrapping
keys to TPM 2.0 data structures for importation into the TPM,
unwrapping keys and exporting them from the TPM, TPM-less
makecredential command and name calculations, TSS2 PEM Key format
support, importing Keys from PEM, DER and SSH formats, conversion from
tpm2-tools based command line strings and loading tpm2-tools context
files.

%description -l pl.UTF-8
Wiązania Pythona TPM2 TSS do bibliotek Enhanced System API (ESYS),
Feature API (FAPI), Marshaling (MU), TCTI Loader (TCTILdr) oraz RC
Decoding (rcdecode). Zawiera także metody narzędziowe do opakowywania
kluczy w struktury danych TPM 2.0 w celu importu do TPM,
rozpakowywania kluczy i eksportowania ich z TPM, obliczeń poleceń i
nazw makecredential bez użycia TPM, obsługi formatu kluczy TSS2 PEM,
importu kluczy z formatów PEM, DER i SSH, konwersji z linii poleceń
tpm2-tools oraz ładowania plików kontekstu tpm2-tools.

%package apidocs
Summary:	API documentation for Python tpm2-pytss module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona tpm2-pytss
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python tpm2-pytss module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona tpm2-pytss.

%prep
%setup -q -n tpm2-pytss-%{version}

# broken and not used (as of 2.1.0)
%{__sed} -i -e '/^\(version\|release\) = /d' docs/conf.py

%build
%py3_build

%if %{with tests}
# test_fapi fail for me (as of 1.2.0) with ibmswtpms2
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
%{__python3} -m pytest test -k 'not test_fapi'
%endif

%if %{with doc}
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%dir %{py3_sitedir}/tpm2_pytss
%{py3_sitedir}/tpm2_pytss/*.py
%attr(755,root,root) %{py3_sitedir}/tpm2_pytss/_libtpm2_pytss.abi3.so
%{py3_sitedir}/tpm2_pytss/__pycache__
%{py3_sitedir}/tpm2_pytss/internal
%{py3_sitedir}/tpm2_pytss-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
