cmake_minimum_required(VERSION 4.2)
project(uebungen)

set(CMAKE_CXX_STANDARD 14)

include_directories(".")

add_executable(uebungen
        "template.cpp"
        "Woche 2/MyTwoCents.cpp"
        "Woche 2/snowflakes.cpp")
