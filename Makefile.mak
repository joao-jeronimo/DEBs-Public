
PYTHON_VERSIONS_TO_BUILD=3.8.15



PYTHON_BUILT_EXECS=$(PYTHON_VERSIONS_TO_BUILD:%=builds/Python-%-build/Python/python)
#PYTHON_MINORS_TO_BUILD=`echo $(PYTHON_VERSIONS_TO_BUILD) | sed 's/^\(.*\)\.[^.]\+$/\1/'`
#PYTHON_INSTALLED_EXECS=$(PYTHON_MINORS_TO_BUILD:%=/odoo/RunTime/Python-%-install/bin/python)

PYTHON_SUPPORTED_VERSIONS=3.8.15 3.7.16
PYTHON_GENERATED_MAKEFILES=$(PYTHON_SUPPORTED_VERSIONS:%=builds/Python-%-build/Makefile)
PYTHON_TARBALLS=$(PYTHON_SUPPORTED_VERSIONS:%=tarballs/Python-%.tar.xz)
UNTARED_MAKEFILES=$(PYTHON_SUPPORTED_VERSIONS:%=untared-%.mak)
PYTHON_UNTARED=`for tarball in $(PYTHON_TARBALLS) ; do tar -tJvf $tarball ; done | sed 's/ \+/ /g' | cut -d" " -f6`

#all-install: $(PYTHON_INSTALLED_EXECS)
all-build: $(PYTHON_BUILT_EXECS)
all-configure: $(PYTHON_GENERATED_MAKEFILES)
all-download: $(PYTHON_TARBALLS)

#$(PYTHON_INSTALLED_EXECS): $(PYTHON_BUILT_EXECS)
#	for built_exec_dir in $(PYTHON_BUILT_EXECS) ; do cd $built_exec_dir && cd .. && make install ; done

builds/Python-%-build/Python/python: builds/Python-%-build/Makefile
	cd `dirname $@` && cd .. && make -j3

builds/Python-%-build/Makefile: src/Python-%/configure
	mkdir -p `dirname $@`
	cd `dirname $@` && ../../src/Python-3.8.15/configure --prefix=/odoo/RunTime/Python-3.8-install/ --enable-optimizations --with-ensurepip=install

src/Python-%/configure: tarballs/Python-%.tar.xz

include $(UNTARED_MAKEFILES)

$(PYTHON_TARBALLS):
	mkdir -p tarballs/
	wget -c "https://www.python.org/ftp/python/$(@:tarballs/Python-%.tar.xz=%)/$(@:tarballs/Python-%.tar.xz=Python-%.tar.xz)" -O $@

untared-%.mak: tarballs/Python-%.tar.xz
	tar -tJvf $< | sed 's/ \+/ /g' | cut -d" " -f6 | sed 's/\(.*\)/src\/\1: tarballs\/$(<:tarballs/Python-%.tar.xz=Python-%.tar.xz)/' > $@

src/Python-%/configure: tarballs/Python-%.tar.xz
	mkdir -p src/
	cd src/ && tar -xJvf ../$< && find . -exec touch {} \;

