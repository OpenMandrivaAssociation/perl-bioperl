%define module	bioperl
%define name	perl-%{module}
%define version 1.5.9
%define release %mkrel 1

%define _requires_exceptions perl(Bio::Expression::FeatureSet)\\|perl(TestInterface)
%define _provides_exceptions perl(Error)\\|perl(Error::Simple)\\|perl(Error::subs)\\|perl(TestInterface)\\|perl(TestObject)

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	BioPerl core modules
Group:		Development/Perl
License:	Artistic
URL:		http://www.bioperl.org
Source:		http://bioperl.org/DIST/BioPerl-%{version}_1.tar.bz2
Patch:		%{module}-1.5.0.makefile.patch
Requires:	perl-Class-MakeMethods
%if %{mdkversion} < 1010
BuildRequires:	perl-devel
%endif
BuildRequires:	perl(Module::Build)
BuildRequires:	perl(Clone)
BuildRequires:	perl(Class::AutoClass)
BuildRequires:	perl(CPAN) >= 1.9205
BuildRequires:  perl(Data::Stag::Writer)
BuildRequires:	perl(GD)
#BuildRequires:	perl(GD::SVG)
BuildRequires:	perl(IO::String)
BuildRequires:	perl(SVG::Graph)
BuildRequires:	perl(Text::Shellwords)
BuildRequires:	perl(Tree::DAG_Node)
BuildRequires:	perl(XML::DOM::XPath)
BuildRequires:	perl(XML::SAX::Writer)
BuildRequires:  perl(XML::Twig)
BuildRequires:	perl(XML::Writer)

Obsoletes:	perl-Bioperl
Provides:	perl-Bioperl
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Officially organized in 1995 and existing informally for several years
prior, The Bioperl Project is an international association of developers
of open source Perl tools for bioinformatics, genomics and life science
research.

%prep
%setup -q -n %{module}-%{version}._1
#%patch
#rm -f t/FeatureIO.t
#rm -f t/SeqFeatCollection.t
#rm -f t/DB.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor <<EOI &>/dev/null
n
a
n
EOI
%make

%check
#%make test

%install
%{__rm} -rf %{buildroot}
%makeinstall_std
# those should belong to Bioperl-Run instead
%{__rm} -f %{buildroot}%{_bindir}/bp_pairwise_kaks.pl
%{__rm} -f %{buildroot}%{_bindir}/bp_blast2tree.pl

# correct permissions
find %{buildroot}%{perl_vendorlib}/Bio/ -name "*.pm" -exec chmod 644 {} \;

# clean doc
executables='.*\(\.\(pl\|cgi\)\|pdf2index\|dbfetch\)$'
for dir in examples doc; do
    find $dir -type f -regex $executables | xargs chmod 644
    find $dir -type f -regex $executables | xargs perl -pi -e 's|^#!/usr/local/bin/perl|#!/usr/bin/perl|'
    find $dir -type f ! -regex $executables | xargs chmod 644
    find $dir -type f | xargs perl -pi -e 'BEGIN {exit unless -T $ARGV[0];} tr/\r//d;'
done

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc examples models
%doc AUTHORS BUGS Changes DEPENDENCIES DEPRECATED INSTALL LICENSE PLATFORMS README
%{_bindir}/*
%{perl_vendorlib}/Bio/
#%{perl_vendorlib}/*.pl
#%{perl_vendorlib}/*.pod
%{_mandir}/*/*


