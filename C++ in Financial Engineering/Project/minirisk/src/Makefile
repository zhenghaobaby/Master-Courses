#
# Possible options
# DEBUG=1                (default is DEBUG=0)
#

# compiler
CC=g++

# platform
PLATFORM := $(shell uname -s)
$(info platform=$(PLATFORM))

# file extensions
ifeq ($(PLATFORM), Linux)
  OBJ=.o
  EXE=.out
  DLL=.so
  LIB=.a
else
# cygwin or mingw
  OBJ=.obj
  EXE=.exe
  DLL=.dll
  LIB=.lib
endif

MAINS := $(wildcard Demo*.cpp) $(wildcard Test*.cpp)
#$(info sources=$(MAINS))
TARGETS := $(patsubst %.cpp,%$(EXE),$(MAINS))
#$(info targets=$(TARGETS))

OBJS := $(patsubst %.cpp,%$(OBJ),$(filter-out $(MAINS), $(wildcard *.cpp)))
#$(info objs=$(OBJS))

HEADERS=$(wildcard *.h)
ALLDEPS=$(HEADERS) Makefile


CFLAGS=-std=c++14 -Wall -Werror -Wconversion -Iinclude
LFLAGS=

ifdef DEBUG
   CFLAGS += -g -DDEBUG
else
   CFLAGS += -O3
endif


all : $(TARGETS)

%$(OBJ) : %.cpp $(ALLDEPS)
	$(CC) -c $(CFLAGS) $< -o $@

.SECONDARY: $(patsubst %.cpp,%$(OBJ),$(wildcard *.cpp))

%.i : %.cpp $(ALLDEPS)
	$(CC) -E -c $(CFLAGS) $< -o $@

%.asm : %.cpp $(ALLDEPS)
	$(CC) -c -g -Wa,-adhln -masm=intel $(CFLAGS) $< > $@


%$(EXE) : %$(OBJ) $(OBJS)
	$(CC) $(LFLAGS) $(OBJS) $< -o $@

# clean
.PHONY: clean
clean:
	rm -f *$(OBJ)  *.i *.ii *.asm *.stackdump *$(EXE)
