https://mechanicalc.com/reference/beam-analysis

class Structure():

    def __init__(self, number_beams, beams_orientation):
        self.number_beams = number_beams            # Number of beams that are supporting the unit
        self.beams_orientation = beams_orientation  # Beams either perpendicular with unit or parallel with unit
