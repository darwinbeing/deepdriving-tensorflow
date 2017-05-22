set(SUBPROJECT "dd-situation-view")

set(${SUBPROJECT}_SOURCE
        src/situation_wrapper.cpp
        src/CSituationView.cpp
        )

set(${SUBPROJECT}_HEADER
        ../common/includes/dd/common/settings.h
        includes/dd/situation/situation_wrapper.h
        src/includes/dd/situation/CSituationView.h
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

target_link_libraries(${SUBPROJECT} ${OpenCV_LIBS})
INSTALL(DIRECTORY "includes" DESTINATION ".")
