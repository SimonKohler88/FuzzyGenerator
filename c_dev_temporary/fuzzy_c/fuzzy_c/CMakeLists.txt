cmake_minimum_required(VERSION 4.3)
project(fuzzy_c C)

set(CMAKE_C_STANDARD 11)

include_directories(.)

add_executable(fuzzy_c
        fuzzy_interface.h
        fuzzy_math.c
        fuzzy_math.h
        main.c
        main.h
        fuzzy_code.c
        fuzzy_code.h)
