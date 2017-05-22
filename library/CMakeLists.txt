cmake_minimum_required(VERSION 3.8)
set(PROJECT "dd")
project(${PROJECT})

add_subdirectory(common)
add_subdirectory(situation)
add_subdirectory(python)

add_custom_target(install_${PROJECT}
        $(MAKE) install
        DEPENDS dd-situation-view
        COMMENT "Installing ${PROJECT}")