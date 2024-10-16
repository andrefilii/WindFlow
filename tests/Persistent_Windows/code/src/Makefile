# Author: Gabriele Mencagli
# Date: 13/01/2020

FF_ROOT         = /home/filippi/libs/fastflow
WF_INCLUDES     = /home/filippi/libs/WindFlow/wf
INCLUDE_DIR     = ../includes
OUT_DIR         = ../bin

CXX             = g++
CXXFLAGS        = -std=c++17
INCLUDES        = -I $(FF_ROOT) -I $(WF_INCLUDES) -I $(INCLUDE_DIR) -I /home/frassinelli/rapidjson/include
MACRO           = -DFF_BOUNDED_BUFFER -DDEFAULT_BUFFER_CAPACITY=4096
OPTFLAGS        = -Ofast -march=native -finline-functions
LDFLAGS         = -pthread -lrocksdb

all: wtest

metric.o: ../includes/util/metric.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(MACRO) $(OPTFLAGS) $< -c

metric_group.o: ../includes/util/metric_group.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(MACRO) $(OPTFLAGS) $< -c

sampler.o: ../includes/util/sampler.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(MACRO) $(OPTFLAGS) $< -c

wtest.o: wtest.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(MACRO) $(OPTFLAGS) $< -c

wtest: metric.o metric_group.o sampler.o wtest.o
	$(CXX) metric.o metric_group.o sampler.o wtest.o -o $(OUT_DIR)/wtest $(LDFLAGS)

clean:
	rm -f $(OUT_DIR)/wtest
	rm -f *.o

.DEFAULT_GOAL := all
.PHONY: all clean
