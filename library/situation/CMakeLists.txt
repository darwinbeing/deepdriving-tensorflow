include(../cmake/library.cmake)

set(SUBPROJECT "dd-situation-view")

set(${SUBPROJECT}_SOURCE
        src/situation_wrapper.cpp
        src/CSituationView.cpp
        src/IndicatorValues.cpp
        src/ImageHelpers.cpp
        src/CSituation.cpp
        )

set(${SUBPROJECT}_HEADER
        ../common/includes/dd/common/settings.h
        ../common/includes/dd/common/datatypes.h
        includes/dd/situation/situation_wrapper.h
        src/includes/dd/situation/CSituationView.h
        src/includes/dd/situation/IndicatorValues.h
        src/includes/dd/situation/ImageHelpers.h
        src/includes/dd/situation/CSituation.h
        )

find_package(OpenCV REQUIRED)
find_package(Boost 1.55 REQUIRED COMPONENTS filesystem date_time)

set(${SUBPROJECT}_INCLUDE_DIRS
        ../common/includes
        includes
        src/includes
        )

DD_ADD_LIBRARY(${SUBPROJECT} "${${SUBPROJECT}_SOURCE}" "${${SUBPROJECT}_HEADER}" "${${SUBPROJECT}_INCLUDE_DIRS}" bin)

INSTALL(DIRECTORY "includes" DESTINATION ".")

target_link_libraries(${SUBPROJECT} ${OpenCV_LIBS})

target_include_directories(${SUBPROJECT} PRIVATE "${Boost_INCLUDE_DIRS}")
target_compile_definitions(${SUBPROJECT} PRIVATE BOOST_ALL_NO_LIB)
target_link_libraries(${SUBPROJECT} Boost::filesystem Boost::date_time)
