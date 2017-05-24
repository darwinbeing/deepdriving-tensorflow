set(SUBPROJECT "dd-drivecontroller")

set(${SUBPROJECT}_SOURCE
        src/controller_wrapper.cpp
        src/CDriveController.cpp
        )

set(${SUBPROJECT}_HEADER
        ../common/includes/dd/common/settings.h
        ../common/includes/dd/common/datatypes.h
        includes/dd/drivecontroller/controller_wrapper.h
        src/includes/dd/drivecontroller/CDriveController.h
        )

set(${SUBPROJECT}_FILES
        ${${SUBPROJECT}_SOURCE}
        ${${SUBPROJECT}_HEADER}
        )

IF(WIN32)
    ADD_DEFINITIONS(-DCOMPILE_DLL)
ENDIF(WIN32)

find_package(OpenCV REQUIRED)

INCLUDE_DIRECTORIES("../common/includes")
INCLUDE_DIRECTORIES("includes")
INCLUDE_DIRECTORIES("src/includes")

IF(${SUBPROJECT}_SOURCE)
    MESSAGE(STATUS "Compile library ${SUBPROJECT}...")
    ADD_LIBRARY(${SUBPROJECT} SHARED ${${SUBPROJECT}_FILES})
    INSTALL(TARGETS ${SUBPROJECT}
            DESTINATION bin)

    add_custom_target(install_${SUBPROJECT}
            $(MAKE) install
            DEPENDS ${SUBPROJECT}
            COMMENT "Installing ${SUBPROJECT}")
ENDIF()

