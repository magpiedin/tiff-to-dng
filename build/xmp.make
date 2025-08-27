# This makefile expects to be run from dng_sdk_1_7_1/xmp/toolkit
# All source & include dirs are releative to TOOLKIT = dng_sdk_1_7_1/xmp/toolkit

ROOT        = ../../../..
TOOLKIT     = .

include $(ROOT)/build/common.make

SOURCE_H    = $(TOOLKIT)/source
PUBLIC_H    = $(TOOLKIT)/public/include
BOOST_H     = $(TOOLKIT)/XMPCore/third-party/boost
PLUGIN_H    = $(TOOLKIT)/XMPFilesPlugins/api/source
INCLUDES    = -I$(PUBLIC_H) -I$(SOURCE_H) -I$(TOOLKIT) -I$(BOOST_H) -I$(PLUGIN_H)

CXXDEFS     = -DUNIX_ENV=1 -DXMP_StaticBuild=1 -DXMP_COMPONENT_INT_NAMESPACE=AdobeXMPCore_Int -DAdobePrivate=1
CXXFLAGS   := $(CXXFLAGS) $(INCLUDES) $(CXXDEFS)

LIB_CPP_FILES := \
        $(wildcard source/*.cpp) \
        $(wildcard third-party/zuid/sources/*.cpp) \
        $(wildcard XMPCore/source/*.cpp) \
        $(wildcard XMPFiles/source/*.cpp) \
        $(wildcard XMPFiles/source/*/*.cpp) \
        $(wildcard XMPFiles/source/*/*/*.cpp)

LIB_OBJ_FILES := $(LIB_CPP_FILES:.cpp=.o)

.PHONY: all clean

$(XMP_LIB): $(LIB_OBJ_FILES)
	$(AR) $(ARFLAGS) $@ $^

clean:
	-rm -f *.o $(XMP_LIB)
