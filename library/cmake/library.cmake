function(DD_ADD_LIBRARY TARGET SOURCE_FILES HEADER_FILES INCLUDE_DIRS DESTINATION)
    #message("TARGET       = ${TARGET}")
    #message("SOURCE_FILES = ${SOURCE_FILES}")
    #message("HEADER_FILES = ${HEADER_FILES}")
    #message("INCLUDE_DIRS  = ${INCLUDE_DIRS}")
    #message("DESTINATION   = ${DESTINATION}")

    set(ALL_FILES
            ${SOURCE_FILES}
            ${HEADER_FILES}
            )

    MESSAGE(STATUS "Compile library ${TARGET}...")

    ADD_LIBRARY(${TARGET} SHARED ${ALL_FILES})

    SET_PROPERTY(TARGET ${TARGET} PROPERTY POSITION_INDEPENDENT_CODE ON)
    
    SET(DEFINES
            )

    IF(WIN32)
        SET(DEFINES
                ${DEFINES}
                COMPILE_DLL
                )
    ENDIF(WIN32)

    MESSAGE(STATUS " * Use Defines: ${DEFINES}")
    target_compile_definitions(${TARGET} PRIVATE ${DEFINES})

    MESSAGE(STATUS " * Use Include-Dirs: ${INCLUDE_DIRS}")
    target_include_directories(${TARGET} PRIVATE ${INCLUDE_DIRS})

    INSTALL(TARGETS ${TARGET}
            DESTINATION ${DESTINATION})

    add_custom_target(install_${TARGET}
            $(MAKE) install
            DEPENDS ${TARGET}
            COMMENT "Installing ${TARGET}")
endfunction()
