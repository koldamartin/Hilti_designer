import math
import numpy as np
from wind import Site
import beams

width_e14 = 1.2 #float(input("Zadejte šířku jednotky [m]: "))
depth_e15 = 0.6 #float(input("Zadejte hloubku jednotky [m]: "))
height_e16 = 2 #float(input("Zadejte výšku jednotky [m]: "))

# _____ load area_____
load_area_e20 = width_e14 * height_e16
print(load_area_e20)

# _____ ratio_____
if width_e14 >= height_e16:
    ratio_e21 = depth_e15 / height_e16
else:
    ratio_e21 = depth_e15 / width_e14
print(ratio_e21)

# _____ force coefficient for rectangular section_____
def force_coefficient_e22():
    if ratio_e21 <= 0.2:
        return 2
    elif ratio_e21 <= 0.7:
        return 2 + ((math.log10(5*ratio_e21))*0.4/math.log10(3.5))
    elif ratio_e21 <= 5:
        return 2.4 - ((math.log10(10/7*ratio_e21))*1.4/math.log10(50/7))
    elif ratio_e21 <= 10:
        return 1 - ((math.log10(0.2*ratio_e21))*0.1/math.log10(2))
    else:
        return 0.9

print(force_coefficient_e22())

# _____ slenderness_____
def slenderness_e23():
    if width_e14 >= height_e16:
        return min(2*width_e14/height_e16, 70)
    else:
        return min(2*height_e16/width_e14, 70)
print(f"Slenderness is {slenderness_e23()} it is a {type(slenderness_e23())}")

# _____ coefficient of final effect___
def final_coef_e24():
    if slenderness_e23() <= 10:
        return 0.6 + math.log10(slenderness_e23())*0.1
    else:
        return 0.7 + (math.log10(slenderness_e23()/10)*0.215/math.log10(7))
print(f"coefficient of final effect: {final_coef_e24()} it is a {type(final_coef_e24())}")

# _____ wind pressure___
site = Site(25,"III",)
wind_pressure_e25 = site.qp(15)
print(f"Tlak větru je {wind_pressure_e25} Pa")

# _____ wind forces___
fw_design_e26 = load_area_e20 * force_coefficient_e22() * final_coef_e24() * wind_pressure_e25/1000 * 1.5
fw_char_e27 = fw_design_e26 / 1.5
print(f"Vodorovná síla od větru (charakteristická) je [kN]: {fw_char_e27} kN")

# _____ movement check_____
self_wght_e31 = 0.4 #float(input("Zadejte tíhu jednotky [kN]: "))
structure_wght_e32 = 0.4 #float(input("Zadejte tíhu konstrukce [kN]: "))
shear_coeff_e33 = 0.78
min_extra_load_e34 = fw_design_e26 / shear_coeff_e33 - (self_wght_e31 + structure_wght_e32)
print(f"Minimální přitížení je F= {min_extra_load_e34} kN")

# _____ flip over check_____
extra_load_e38 = 5 #float(input("Zadejte přitížení [kN]: "))
total_wght_e39 = self_wght_e31 + structure_wght_e32 + extra_load_e38
structure_hght_e40 = 0.75 #float(input("Zadejte výšku konstrukce [m]: "))
grvt_center_e41 = structure_hght_e40 + height_e16/2
rotation_dstnc_e42 = fw_design_e26 * grvt_center_e41 / total_wght_e39
min_columns_dstnc_e43 = 2 * rotation_dstnc_e42
print(f"Minimální rozpětí stojek je {min_columns_dstnc_e43} m")

# _____ final loads to enter into calculation_____
# Case I - the unit is resting on perpendicular beams
beams_number_e47 = 2 #int(input("Zadejte počet nosníků na kterých jednotka stojí [ks]: "))

if beams_number_e47 == 1:
    raise Exception("Jednotka nesmí ležet jen na jednom nosníku!")
elif beams_number_e47 == 2:
    horiz_force_edge_e48 = fw_char_e27 / beams_number_e47
    horiz_force_mid_e49 = 0
    horiz_force_mid_e56 = 0
    vert_force_mid_e57 = 0
else:
    horiz_force_edge_e48 = fw_char_e27 / (beams_number_e47 - 1) / 2
    horiz_force_mid_e49 = fw_char_e27 / (beams_number_e47 - 1)
    horiz_force_mid_e56 = horiz_force_mid_e49 / 2
    vert_force_mid_e57 = horiz_force_mid_e49 * height_e16 / 2 / depth_e15
    print(f"Horizontální síla na prostřední nosník: {horiz_force_mid_e56} kN")
    print(f"Vertikální síla na prostřední nosník: {vert_force_mid_e57} kN")
horiz_force_edge_e52 = horiz_force_edge_e48 / 2
vert_force_edge_e53 = horiz_force_edge_e48 * height_e16 / 2 / depth_e15
print(f"Horizontální síla na krajní rám: {horiz_force_edge_e52} kN")
print(f"Vertikální síla na krajní rám: {vert_force_edge_e53} kN")

# Forces to export
self_weight_1 = self_wght_e31 / 4 #kN
wind_vert = max(vert_force_edge_e53, vert_force_mid_e57) #kN
wind_horiz = max(horiz_force_edge_e52, horiz_force_mid_e56) #kN
real_span = max(min_columns_dstnc_e43, depth_e15) #m

# Ultimate limit state calculation
a = (real_span - depth_e15) / 2 #m
MEd_self_weight = self_weight_1*1.35 * a
MEd_wind = wind_vert*1.5 * depth_e15 / 2
MEd = MEd_wind + MEd_self_weight
if MEd > list(beams.permissable_moment.items())[-1][1]: #This will check if the biggest has bigger MRd than MEd
    print(list(beams.permissable_moment.items())[-1][1])
    raise Exception(f"Nosník nelze navrhnout, selhání při MSÚ je {MEd/list(beams.permissable_moment.items())[-1][1]*100}%")
else:
    for section in beams.permtion_modulus:
        beam = beams.Beam(section, real_span)
        if beam.permissable_moment > MEd:
            print(f"\nPoužijte nosník {section}, MRd = {beam.permissable_moment} kNm, MEd = {MEd} kNm")
            print(f"Využití nosníku při MSÚ je {MEd/beam.permissable_moment*100}%\n")
            break
        else:
            pass

    # Serviceability limit state calculation
    # TODO: pruhyb mozna prepocitat timhle https://www.structuralbasics.com/beam-deflection-formulas/
    for section in beams.permtion_modulus:
        beam = beams.Beam(section, real_span)
        delta_self_weight = (self_weight_1 * a) / (24*beams.E*1000*beam.moment_of_inertia/(1000**4))*(3*real_span**2 - 4*a**2) #m
        delta_wind = 0 #This will find the distance from a support {x} where the deflection from wind is maximal
        for x in np.arange(0, real_span, 0.1):
            delta_wind_actual = wind_vert*depth_e15*x/(24*real_span*beams.E*1000*beam.moment_of_inertia/(1000**4))*(real_span**2 - 4*x**2) #m
            if delta_wind_actual > delta_wind:
                delta_wind = delta_wind_actual
    # TODO: Udelat for loop, tak aby to tisklo jen nosnik ktery vyhovi na MSP,stejne jako v MSU

        print(f"Průhyb {section} od vlastní tíhy je {delta_self_weight*1000} mm a limitní průhyb je {beam.deformation_limit*1000} mm")
        print(f"Průhyb {section} od větru je {delta_wind * 1000} mm a limitní průhyb je {beam.deformation_limit * 1000} mm")
        print(f"Využití nosníku při MSP je {(delta_self_weight+delta_wind) / beam.deformation_limit * 100}%\n")

# TODO: Overit vypocty v MSE
