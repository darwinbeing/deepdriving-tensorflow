set(SUBPROJECT "dd-common")

set(${SUBPROJECT}_SOURCE)

set(${SUBPROJECT}_HEADER
        includes/dd/common/settings.h
        includes/dd/common/datatypes.h
        )

set(${SUBPROJECT}_FILES
        ${${SUBPROJECT}_SOURCE}
        ${${SUBPROJECT}_HEADER}
        )

IF(WIN32)
    ADD_DEFINITIONS(-DCOMPILE_DLL)
ENDIF(WIN32)

INCLUDE_DIRECTORIES("includes")

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

INSTALL(DIRECTORY "includes" DESTINATION ".")

