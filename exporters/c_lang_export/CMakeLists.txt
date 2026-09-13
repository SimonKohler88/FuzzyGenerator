cmake_minimum_required(VERSION 4.3)
project(c_lang_export C)

set(CMAKE_C_STANDARD 11)

include_directories(.)
include_directories(working_dir)

add_executable(c_lang_export
        working_dir/tst_prj_name.c
        working_dir/tst_prj_name.h
        fuzzy_interface.h
        fuzzy_math.c
        fuzzy_math.h
        main.c)
