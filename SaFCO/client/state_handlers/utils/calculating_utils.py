#!/usr/bin/env python3
from math import sin, cos, asin, sqrt


# def calculate_scale(first_coordinates, second_coordinates):
#     if first_coordinates is None or second_coordinates is None:
#         return
#     if len(first_coordinates) < 2 or len(second_coordinates) < 2:
#         return
#     cathetus_sqr1 = abs(first_coordinates[0][0] - first_coordinates[1][0]) ** 2
#     cathetus_sqr2 = abs(first_coordinates[0][1] - first_coordinates[1][1]) ** 2
#     first_line_length = sqrt(cathetus_sqr1 + cathetus_sqr2)
#     cathetus_sqr1 = abs(second_coordinates[0][0] - second_coordinates[1][0]) ** 2
#     cathetus_sqr2 = abs(second_coordinates[0][1] - second_coordinates[1][1]) ** 2
#     second_line_length = sqrt(cathetus_sqr1 + cathetus_sqr2)
#
#     scale = first_line_length / second_line_length
#     return (scale, scale)


def calculate_scale(circuit_coordinates, image_coordinates):
    a_r, b_r = circuit_coordinates
    a_i, b_i = image_coordinates
    # scale = abs(a_r[0] - b_r[0]) / abs(a_i[0] - b_i[0])
    scale_r = sqrt((a_r[0] - b_r[0]) ** 2 + (a_r[1] - b_r[1]) ** 2)
    scale_i = sqrt((a_i[0] - b_i[0]) ** 2 + (a_i[1] - b_i[1]) ** 2)
    scale = scale_r / scale_i
    return (scale, scale)


def translate_coordinates(circuit_coordinates, image_coordinates, scale, point):
    a_r, b_r = circuit_coordinates
    a_i, b_i = image_coordinates
    point_r_not_rotated = (a_r[0] - (point[1] - a_i[1]) * scale[1],
                           a_r[1] + (point[0] - a_i[0]) * scale[0])
    # angle_i = asin((a_i[1] - b_i[1]) / sqrt((a_i[0] - b_i[0]) ** 2 + (a_i[1] - b_i[1]) ** 2))
    # angle_r = asin((a_r[1] - b_r[1]) / sqrt((a_r[0] - b_r[0]) ** 2 + (a_r[1] - b_r[1]) ** 2))
    # diff_angle = angle_i - angle_r
    # c_r = (cos(diff_angle) * point_r_not_rotated[0], sin(diff_angle) * point_r_not_rotated[1])
    return point_r_not_rotated

    if __name__ == '__main__':
        a_r = ()
