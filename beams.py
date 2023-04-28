steel_yield = 280 / 1.1  # MPa
E = 210000 #MPa
moment_inertia = {"MT40": 57700, "MT50": 70400, "MT60": 286700, "MT40D": 299600}  # mm4
permtion_modulus = {"MT40": 2650, "MT50": 3190, "MT40D": 7050, "MT60": 7830}  # mm3
permissable_moment = {key: value * steel_yield / 1000000 for (key, value) in permtion_modulus.items()}  # kNm

class Beam():
    def __init__(self, type, span):
        self.type = type
        self.moment_of_inertia = moment_inertia[type]
        self.permissable_moment = permissable_moment[type]
        self.deformation_limit = span/250
        self.span = span
