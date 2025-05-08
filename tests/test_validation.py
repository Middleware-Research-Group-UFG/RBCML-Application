from ..app.validation import validate_model

model = {
        "roles": ["student", "professor", "principal"],
        "connections": {
            "principal-professor-student": [
                [True, True, True, True, True, True, True, True],
                [False, False, True, True, True, True, False, False],
                [False, False, False, False, True, True, False, False]
            ],
            "professor-student": [
                [False, False, False, False, True, True, False, False], 
                [True, True, True, True, True, True, True, True]
              ]
        }
}

model2 = {
        "roles": ["student", "professor", "principal"],
        "connections": {
            "principal-professor-student": [
                [True, True, True, True, True, True, True, True],
                [False, False, True, True, True, True, False, False],
                [False, False, False, False, True, True, False, False]
            ]
          }
}

model3 = {
        "roles": ["student", "professor", "principal"],
        "connections": {
            "principal-professor-student": [
                [True, True, True, True, True, True, True, True],
                [False, False, True, True, "True", True, False, False],
                [False, False, False, False, True, True, False, False]
            ]
          }
}

model4 = {
        "roles": ["student", "professor", "principal"],
        "connections": {
            "student-principal-professor": [
                [True, True, True, True, True, True, True, True],
                [False, False, True, True, True, True, False, False],
                [False, False, False, False, True, True, False, False]
            ]
          }
}

assert validate_model(model) == True
assert validate_model(model2) == True
assert validate_model(model3) == False
assert validate_model(model4) == False
