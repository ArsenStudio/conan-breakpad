cmake_minimum_required(VERSION 2.8.11)
project(test_package)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_library(BREAKPAD NAMES Breakpad)
if (NOT BREAKPAD)
  message(FATAL_ERROR "Breakpad not found")
endif()

include_directories(${BREAKPAD_INCLUDE_DIRS})

file(GLOB SOURCE_FILES *.cpp)

add_executable(${PROJECT_NAME} ${SOURCE_FILES})
target_link_libraries(${PROJECT_NAME} ${BREAKPAD_LIBRARIES})