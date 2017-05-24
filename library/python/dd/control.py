import ctypes

class Control_t(ctypes.Structure):
    _fields_ = [
        ('Steering',     ctypes.c_double),
        ('Accelerating', ctypes.c_double),
        ('Breaking',     ctypes.c_double),
    ]


    def __init__(self):
        self.Steering     = 0
        self.Accelerating = 0
        self.Breaking     = 0


    def __str__(self):
        String = ""
        String += "Steering={}\n".format(self.Steering)
        String += "Accelerating={}\n".format(self.Accelerating)
        String += "Breaking={}\n".format(self.Breaking)
        return String
