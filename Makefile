CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -O2
INCLUDES = -Idng_sdk_1_7_1/dng_sdk/source -Idng_sdk_1_7_1/libjxl/libjxl

all: dng_validate.o

dng_validate.o: dng_sdk_1_7_1/dng_sdk/source/dng_validate.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c -o $@ $<
