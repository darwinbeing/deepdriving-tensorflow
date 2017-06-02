include(../cmake/library.cmake)

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

set(${SUBPROJECT}_INCLUDE_DIRS
        ../common/includes
        includes
        src/includes
        )

DD_ADD_LIBRARY(${SUBPROJECT} "${${SUBPROJECT}_SOURCE}" "${${SUBPROJECT}_HEADER}" "${${SUBPROJECT}_INCLUDE_DIRS}" bin)

INSTALL(DIRECTORY "includes" DESTINATION ".")
