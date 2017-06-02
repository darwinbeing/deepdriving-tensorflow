cmake_minimum_required(VERSION 3.8)
set(PROJECT "dd")
project(${PROJECT})

add_subdirectory(common)
add_subdirectory(situation)
add_subdirectory(python)
add_subdirectory(drivecontroller)
add_subdirectory(leveldb)
add_subdirectory(datareader)
add_dependencies(dd-datareader leveldb)

add_custom_target(install_${PROJECT}
        $(MAKE) install
        DEPENDS dd-situation-view dd-drivecontroller leveldb dd-datareader
        COMMENT "Installing ${PROJECT}")