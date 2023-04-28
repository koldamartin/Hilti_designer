from forces import self_weight_1, wind_vert, wind_horiz, real_span
from beams import Beam

beam = Beam("MT40", real_span)
print(beam.span)
print(beam.deformation_limit)
print(beam.permissable_moment)