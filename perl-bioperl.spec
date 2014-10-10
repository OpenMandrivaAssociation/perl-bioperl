%define upstream_name BioPerl
%define upstream_version 1.6.901

%if %{_use_internal_dependency_generator}
%define __noautoreq 'perl\\(Bio::Expression::(.*)\\)|perl\\(Bio::Phylo::(.*)\\)|perl\\(Mac::(.*)\\)|perl\\(Win32::Clipboard\\)|perl\\(Bio::Tools::Run::Samtools\\)|perl\\(TestInterface\\)'
%define __noautoprov 'perl\\(Error\\)|perl\\(Error::Simple\\)|perl\\(Error::subs\\)|perl\\(TestInterface\\)|perl\\(TestObject\\)'
%else
%define _requires_exceptions perl(Bio::Expression::FeatureSet)\\|perl(TestInterface)
%define _provides_exceptions perl(Error)\\|perl(Error::Simple)\\|perl(Error::subs)\\|perl(TestInterface)\\|perl(TestObject)
%endif

Name:		perl-bioperl
Version:	%{upstream_version}
Release:	8
Summary:	BioPerl core modules
Group:		Development/Perl
License:	Artistic
URL:		http://www.bioperl.org
Source0:	http://bioperl.org/DIST/%{upstream_name}-%{upstream_version}.tar.gz

BuildRequires:	perl-devel
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
%rename	perl-Bioperl

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

perl Build.PL --installdirs vendor --destdir %{buildroot}  <<EOI
a
n
EOI


%check
#./Build test
#%make test

%install
./Build install
#makeinstall_std
# those should belong to Bioperl-Run instead
rm -f %{buildroot}%{_bindir}/bp_pairwise_kaks.pl
rm -f %{buildroot}%{_bindir}/bp_blast2tree.pl

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

%files
%doc examples models
%doc AUTHORS BUGS Changes DEPENDENCIES DEPRECATED INSTALL LICENSE README README.urpmi
%{_bindir}/*
%{perl_vendorlib}/Bio/
%{_mandir}/*/*


%changelog
* Tue Jan 24 2012 StÃ©phane TÃ©letchÃ©a <steletch@mandriva.org> 1.6.901-2mdv2012.0
+ Revision: 768075
- Rebuild for new perl

* Tue Sep 20 2011 StÃ©phane TÃ©letchÃ©a <steletch@mandriva.org> 1.6.901-1
+ Revision: 700499
- Skip tests since some require a valid internet connection
- Update to 1.6.901
- Drop pre-10.1 support
- update BR for a more complete bioperl experience
- indicate to what corresponds default building choices
- copy the default bash variables for databases
- add bioperl scripts

* Wed Sep 30 2009 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 1.6.1-1mdv2010.0
+ Revision: 451789
- update to 1.6.1

* Sat Jul 25 2009 JÃ©rÃ´me Quelin <jquelin@mandriva.org> 1.6.0-2mdv2010.0
+ Revision: 399778
- adding missing buildrequires:
- adding missing buildrequires:
- adding missing buildrequires:
- fixed spec file to build correctly
- using %%perl_convert_version

  + StÃ©phane TÃ©letchÃ©a <steletch@mandriva.org>
    - Add missing interactive answer
    - Added versioned dependency on autoclass
    - Corrected dependencies
    - Added perl-Algorithm-Munkres requirement

* Mon Jan 26 2009 StÃ©phane TÃ©letchÃ©a <steletch@mandriva.org> 1.6.0-1mdv2009.1
+ Revision: 333774
- Update to 1.6.0 final
- Removed unused patch

* Tue Dec 30 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.5.9-1mdv2009.1
+ Revision: 321400
- new version

* Wed Jul 30 2008 Thierry Vignaud <tv@mandriva.org> 1.5.2_102-3mdv2009.0
+ Revision: 255439
- rebuild

* Fri Jan 11 2008 StÃ©phane TÃ©letchÃ©a <steletch@mandriva.org> 1.5.2_102-1mdv2008.1
+ Revision: 148695
- Disable tests due to stange failure in bs
- CPAN should not be triggered now since we have all necessary dependencies
- added basic default options for scripts and extra plugins
- Add BuildRequires for iurt
- Add a stronger dependency on CPAN version
- Update to 1.5.2_102
- Added some dependencies (perl-GD-SVG still missing)
- Tests enabled since the new perl @INC search order allows to get the latest modules first
- Fix some permissions in doc
- Correct included files in docdir

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Tue Mar 13 2007 Pixel <pixel@mandriva.com> 1.5.1-5mdv2007.1
+ Revision: 142178
- quick and dirty workaround of rpm find-provides and find-requires looking
  for things even in /usr/share/doc/.../examples/...
- hack: disabling "make test" so that build works

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - Import perl-bioperl

* Fri May 05 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.5.1-4mdk
- better buildrequires syntax 
- more buildrequires

* Fri Mar 24 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.5.1-3mdk
- buildrequires

* Mon Mar 20 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.5.1-2mdk
- fix dependencies

* Wed Jan 11 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.5.1-1mdk
- new version
- fixed doc files perms, encoding and shellbang
- don't install scripts in documentation, they are already installed in /usr/bin

* Tue Jan 03 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1.5.0-4mdk
- Add BuildRequires

* Tue Dec 27 2005 Guillaume Rousse <guillomovitch@mandriva.org> 1.5.0-3mdk
- corrected name
- %%mkrel
- enable test, except failing one

* Tue Jun 07 2005 Nicolas Lécureuil <neoclust@mandriva.org> 1.5.0-2mdk
- rebuild for new Perl

* Thu Jan 27 2005 Guillaume Rousse <guillomovitch@mandrake.org> 1.5.0-1mdk 
- new version
- generate man pages
- spec cleanup

* Mon Dec 20 2004 Guillaume Rousse <guillomovitch@mandrake.org> 1.4-4mdk
- fix buildrequires in a backward compatible way

* Thu Jul 22 2004 Guillaume Rousse <guillomovitch@mandrake.org> 1.4-3mdk 
- rpmbuildupdate aware

