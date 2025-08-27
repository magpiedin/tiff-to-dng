# This makefile calls make on other makefiles (in ../build) to build things

include ../build/common.make

all: libs dng_validate
		ls -l ./bin
		@echo "\n*** success ***\n"

# Targets to build the libraries
#
libxmp:
		cd $(DNGSDK)/xmp/toolkit; \
		make -f ../../../../build/xmp.make $(XMP_LIB)
		cp $(DNGSDK)/xmp/toolkit/$(XMP_LIB) ./lib

libdng:
		cd $(DNGSDK)/dng_sdk/source; \
		make -f ../../../../build/dng.make $(DNG_LIB)
		cp $(DNGSDK)/dng_sdk/source/$(DNG_LIB) ./lib
		cp $(DNGSDK)/dng_sdk/source/*.h ./include

libs: libxmp libdng


# Target to build Adobe's command line tool, dng_validate
#
dng_validate:
		cd $(DNGSDK)/dng_sdk/source; \
		make -f ../../../../build/dng.make dng_validate
		mv $(DNGSDK)/dng_sdk/source/dng_validate ./bin

clean:
		-rm -rf ./lib/* ./bin/* ./include/*

.PHONY: all libs libxmp libdng dng_validate clean
