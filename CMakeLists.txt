cmake_minimum_required(VERSION 3.17)
project(serd VERSION 0.30.17)

include(cmake/boilerplate_init.cmake)
boilerplate_init()

add_library(serd
        src/base64.c
        src/byte_source.c
        src/env.c
        src/n3.c
        src/node.c
        src/reader.c
        src/string.c
        src/system.c
        src/uri.c
        src/writer.c
        )
add_library(serd::serd ALIAS serd)

target_include_directories(serd PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        PRIVATE
        src)

set_target_properties(serd PROPERTIES
        C_STANDARD 99
        VERSION ${PROJECT_VERSION}
        SOVERSION ${PROJECT_VERSION_MAJOR}
        )

target_compile_options(serd PRIVATE -Wall -Wpedantic -Wextra -Wno-nullability-extension)

if (IS_TOP_LEVEL)
    include(cmake/install_library.cmake)
    install_cpp_library(serd include)
endif ()
