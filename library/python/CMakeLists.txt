set(SUBPROJECT "dd-python")

set(PYTHON_EXAMPLES
        examples/example_situation_view.py
        examples/example_drivecontroller.py
        examples/example_datareader.py
        )

INSTALL(FILES ${PYTHON_EXAMPLES} DESTINATION "python")
INSTALL(DIRECTORY "dd" DESTINATION "python")

