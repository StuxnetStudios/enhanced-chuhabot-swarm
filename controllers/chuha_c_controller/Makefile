# Makefile for ChuhaBot C-based Swarm Controller
# Optimized for Webots simulation environment

# Default target
.PHONY: release debug clean

# Use environment variable WEBOTS_HOME if it exists
# Otherwise use the default installation path
ifdef WEBOTS_HOME
  WEBOTS_PATH = $(WEBOTS_HOME)
else
  ifeq ($(OS),Windows_NT)
    WEBOTS_PATH = C:/Program Files/Webots
  else
    WEBOTS_PATH = /usr/local/webots
  endif
endif

# Compiler settings
ifeq ($(OS),Windows_NT)
  CC = gcc
  EXTRA_FLAGS = -mwindows
else
  CC = gcc
endif

# Include and library paths
INCLUDE = -I"$(WEBOTS_PATH)/include/controller/c"
LIBS = -L"$(WEBOTS_PATH)/lib/controller" -lController

# Compiler flags
CFLAGS = -Wall -O2 -std=c99 $(INCLUDE) $(EXTRA_FLAGS)
DEBUG_CFLAGS = -Wall -g -std=c99 $(INCLUDE) $(EXTRA_FLAGS) -DDEBUG

# Source and target
SOURCE = chuha_c_controller.c
TARGET = chuha_c_controller
DEBUG_TARGET = $(TARGET)_debug

# Default target - optimized release build
release: $(TARGET)

# Debug build
debug: $(DEBUG_TARGET)

# Release build rule
$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) -o $(TARGET) $(SOURCE) $(LIBS)
	@echo "Built release version: $(TARGET)"

# Debug build rule
$(DEBUG_TARGET): $(SOURCE)
	$(CC) $(DEBUG_CFLAGS) -o $(DEBUG_TARGET) $(SOURCE) $(LIBS)
	@echo "Built debug version: $(DEBUG_TARGET)"

# Clean build files
clean:
	@echo "Cleaning build files..."
ifeq ($(OS),Windows_NT)
	@if exist $(TARGET).exe del $(TARGET).exe
	@if exist $(DEBUG_TARGET).exe del $(DEBUG_TARGET).exe
else
	@rm -f $(TARGET) $(DEBUG_TARGET)
endif
	@echo "Clean complete"

# Help target
help:
	@echo "ChuhaBot C Controller Build System"
	@echo "=================================="
	@echo "Available targets:"
	@echo "  release  - Build optimized version (default)"
	@echo "  debug    - Build debug version with symbols"
	@echo "  clean    - Remove build files"
	@echo "  help     - Show this help"
	@echo ""
	@echo "Environment variables:"
	@echo "  WEBOTS_HOME - Path to Webots installation"
	@echo "                (defaults to system installation)"
	@echo ""
	@echo "Usage examples:"
	@echo "  make           # Build release version"
	@echo "  make debug     # Build debug version"
	@echo "  make clean     # Clean build files"
