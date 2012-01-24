%define upstream_name    BioPerl
%define rpm_name         perl-bioperl
%define upstream_version 1.6.901

%define _requires_exceptions perl(Bio::Expression::FeatureSet)\\|perl(TestInterface)
%define _provides_exceptions perl(Error)\\|perl(Error::Simple)\\|perl(Error::subs)\\|perl(TestInterface)\\|perl(TestObject)

Name:		%{rpm_name}
# Version:	%perl_convert_version %{upstream_version}
Version:	%{upstream_version}
Release:	%mkrel 2

Summary:	BioPerl core modules
Group:		Development/Perl
License:	Artistic
URL:		http://www.bioperl.org
Source0:	http://bioperl.org/DIST/%{upstream_name}-%{upstream_version}.tar.gz

#if %{mdkversion} < 1010
#BuildRequires:	perl-devel
#endif
BuildRequires:	perl(Algorithm::Munkres)
BuildRequires:	perl(Array::Compare)
BuildRequires:	perl(Clone)
BuildRequires:	perl(Convert::Binary::C)
BuildRequires:	perl(CPAN) >= 1.920.5
BuildRequires:	perl(Data::Stag)
BuildRequires:	perl(DB_File)
BuildRequires:	perl(GraphViz)
BuildRequires:	perl(IO::String)
BuildRequires:	perl(LWP::UserAgent)
BuildRequires:	perl(Math::Random)
BuildRequires:	perl(Module::Build)
BuildRequires:	perl(Spreadsheet::ParseExcel)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Set::Scalar)
BuildRequires:	perl(Sort::Naturally)
BuildRequires:	perl(SVG::Graph)
BuildRequires:	perl(XML::DOM::XPath)
BuildRequires:	perl(XML::SAX::Writer)
BuildRequires:	perl(XML::Simple)
BuildRequires:	perl(XML::Writer)

BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}
Obsoletes:	perl-Bioperl
Provides:	perl-Bioperl


Requires:	perl(Class::AutoClass) >= 1.01
#Requires:	perl(Class::MakeMethod)
#Requires:	perl(Data::Stag::Writer)
Requires:	perl(GD)
#Requires:	perl(GD::SVG)
#Requires:	perl(IO::String)
#Requires:	perl(SVG::Graph)
Requires:	perl(SOAP::Lite)
Requires:	perl(Text::Shellwords)
#Requires:	perl(Tree::DAG_Node)
#Requires:	perl(XML::DOM::XPath)
#Requires:	perl(XML::SAX::Writer)
#Requires:	perl(XML::Twig)
#Requires:	perl(XML::Writer)

%description
Officially organized in 1995 and existing informally for several years
prior, The Bioperl Project is an international association of developers
of open source Perl tools for bioinformatics, genomics and life science
research.

%prep
%setup -q -n %{upstream_name}-%{upstream_version}

%build
# Here are the default values for the installation:
# Install [a]ll BioPerl scripts, [n]one, or choose groups [i]nteractively? [a]
# Do you want to run tests that require connection to servers across the internet
# (likely to cause some failures)? y/n [n] n

%{__perl} Build.PL --installdirs vendor --destdir %buildroot  <<EOI
a
n
EOI


%check
#./Build test
#%make test

%install
%{__rm} -rf %{buildroot}
./Build install
#makeinstall_std
# those should belong to Bioperl-Run instead
%{__rm} -f %{buildroot}%{_bindir}/bp_pairwise_kaks.pl
%{__rm} -f %{buildroot}%{_bindir}/bp_blast2tree.pl

# correct permissions
find %{buildroot}%{perl_vendorlib}/Bio/ -name "*.pm" -exec chmod 644 {} \;

# clean doc
executables='.*\(\.\(pl\|cgi\)\|pdf2index\|dbfetch\)$'
for dir in examples doc;
do
	find $dir -type f -regex $executables | xargs chmod 644
	find $dir -type f -regex $executables | xargs perl -pi -e 's|^#!/usr/local/bin/perl|#!/usr/bin/perl|'
	find $dir -type f ! -regex $executables | xargs chmod 644
	find $dir -type f | xargs perl -pi -e 'BEGIN {exit unless -T $ARGV[0];} tr/\r//d;'
done

cat << EOD > README.urpmi
    Environment Variables

Some modules which run external programs need certain environment
variables set. If you do not have a local copy of the specific
executable you do not need to set these variables. Additionally the
modules will attempt to locate the specific applications in your
runtime PATH variable. You may also need to set an environment
variable to tell BioPerl about your network configuration if your site
uses a firewall.

Setting environment variables on unix means adding lines like the
following to your shell *rc file.

   For bash or sh:

 export BLASTDIR=/data1/blast

   For csh or tcsh:

 setenv BLASTDIR /data1/blast

Some environment variables include:

+------------------------------------------------------------------------+
| Env. Variable |                      Description                       |
|---------------+--------------------------------------------------------|
|               |Specifies where the NCBI blastall, blastpgp, bl2seq,    |
|BLASTDIR       |etc.. are located. A 'data' directory could also be     |
|               |present in this directory as well, you could put your   |
|               |blastable databases here.                               |
|---------------+--------------------------------------------------------|
|               |If one does not want to locate the data dir within the  |
|BLASTDATADIR or|same dir as where the BLASTDIR variable points, a       |
|BLASTDB        |BLASTDATADIR or BLASTDB variable can be set to point to |
|               |a dir where BLAST database indexes are located.         |
|---------------+--------------------------------------------------------|
|BLASTMAT       |The directory containing the substitution matrices such |
|               |as BLOSUM62.                                            |
|---------------+--------------------------------------------------------|
|CLUSTALDIR     |The directory where the clustalw executable is located. |
|---------------+--------------------------------------------------------|
|TCOFFEEDIR     |The directory where the t_coffee executable is located. |
|---------------+--------------------------------------------------------|
|               |If you access the internet via a proxy server then you  |
|               |can tell the BioPerl modules which require network      |
|               |access about this by using the http_proxy environment   |
|http_proxy     |variable. The value set includes the proxy address and  |
|               |the port, with optional username/password for           |
|               |authentication purposes                                 |
|               |(e.g. http://USERNAME:PASSWORD@proxy.example.com:8080). |
+------------------------------------------------------------------------+
EOD

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc examples models
%doc AUTHORS BUGS Changes DEPENDENCIES DEPRECATED INSTALL LICENSE README README.urpmi
%_bindir/*
%{perl_vendorlib}/Bio/
#{perl_vendorlib}/*.pl
#{perl_vendorlib}/*.pod
%{_mandir}/*/*
