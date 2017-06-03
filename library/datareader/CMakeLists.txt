include(../cmake/library.cmake)

set(SUBPROJECT "dd-datareader")

set(${SUBPROJECT}_SOURCE
        src/datareader_wrapper.cpp
        src/CDataReader.cpp
        src/CDataEntry.cpp
        src/CProtoMessage.cpp
        )

set(${SUBPROJECT}_HEADER
        ../common/includes/dd/common/settings.h
        ../common/includes/dd/common/datatypes.h
        includes/dd/datareader/datareader_wrapper.h
        )

set(${SUBPROJECT}_INCLUDE_DIRS
        ../common/includes
        includes
        src/includes
        )

DD_ADD_LIBRARY(${SUBPROJECT} "${${SUBPROJECT}_SOURCE}" "${${SUBPROJECT}_HEADER}" "${${SUBPROJECT}_INCLUDE_DIRS}" bin)

target_link_libraries(${SUBPROJECT} leveldb)

INSTALL(DIRECTORY "includes" DESTINATION ".")