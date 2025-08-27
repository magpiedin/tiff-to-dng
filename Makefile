CXX = g++
CXXFLAGS = -std=c++11 -I. -O2 -pipe
LDFLAGS = -ljpeg -lz -lpthread -ldl

DNG_SDK_DIR = dng_sdk_1_7_1
DNG_SOURCE_DIR = $(DNG_SDK_DIR)/dng_sdk/source
XMP_DIR = $(DNG_SDK_DIR)/xmp/toolkit
JPEG_DIR = $(DNG_SDK_DIR)/libjpeg

INCLUDES = -I$(DNG_SOURCE_DIR) \
           -I$(XMP_DIR)/public/include \
           -I$(JPEG_DIR)

DEFS = -DUNIX_ENV=1 -DXMP_StaticBuild=1 -DqDNGValidateTarget=1 -DqDNGUseLibJPEG=1 -DqDNGUseXMP=1 -DqDNGThreadSafe=1

DNG_SRCS = $(wildcard $(DNG_SOURCE_DIR)/*.cpp)
XMP_SRCS = $(wildcard $(XMP_DIR)/XMPCore/source/*.cpp) \
           $(wildcard $(XMP_DIR)/XMPCommon/source/*.cpp) \
           $(wildcard $(XMP_DIR)/source/*.cpp)
JPEG_SRCS = $(wildcard $(JPEG_DIR)/*.c)

SRCS = $(DNG_SRCS) $(XMP_SRCS) $(JPEG_SRCS)
OBJS = $(SRCS:.cpp=.o)
OBJS := $(OBJS:.c=.o)

TARGET = dng_validate

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(OBJS) -o $(TARGET) $(LDFLAGS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(DEFS) -c $< -o $@

%.o: %.c
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(DEFS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)
