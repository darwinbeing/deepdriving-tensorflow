set(SUBPROJECT "dd-python")

set(PYTHON_EXAMPLES
        examples/example_situation_view.py)

INSTALL(FILES ${PYTHON_EXAMPLES} DESTINATION "python")
INSTALL(DIRECTORY "dd_situation_view" DESTINATION "python")

