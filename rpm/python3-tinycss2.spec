# Adapted for SaifishOS
# + Disable check by default
# + Remove redundant python-tinycss2
%define srcname tinycss2


%global py3_prefix python3


Name:           python3-%{srcname}
Version:        1.1.1
Release:        1
Summary:        Low-level CSS parser for Python

License:        BSD
URL:            https://pypi.python.org/pypi/%{srcname}/
Source0:        %{name}-%{version}.tar.gz
# Fedora does not ship pytest's flake8/isort modules
#Patch0:         %%{name}-disable-flake8-isort-for-pytest.patch

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
# used as "build-backend" in pyproject.toml but not detected by Fedora's
# macros to generate build requirements
BuildRequires:  python3-flit
BuildRequires:  python3dist(toml)
BuildRequires:  python3dist(pip)
BuildRequires:  python3dist(webencodings)

Requires:       %{py3_prefix}-webencodings >= 0.4
%{?python_provide:%python_provide %{py3_prefix}-%{srcname}}

%description
tinycss2 is a modern, low-level CSS parser for Python. tinycss2 is a rewrite of
tinycss with a simpler API, based on the more recent CSS Syntax Level 3
specification.

%global _version %(echo %{version}|sed -e 's/\+.*//')

%prep
%autosetup -n %{name}-%{version}/upstream

#%%generate_buildrequires
%pyproject_buildrequires -r -x test


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files tinycss2


%check
%if %{with check}
%{pytest}
# remove files which are only required for unit tests (including test.pyc/.pyo)
rm -rf %{buildroot}%{python3_sitelib}/%{srcname}/css-parsing-tests
rm -rf %{buildroot}%{python3_sitelib}/%{srcname}/test.py
rm -rf %{buildroot}%{python3_sitelib}/%{srcname}/__pycache__/test.*.py?
%endif

%files -n %{py3_prefix}-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.rst
