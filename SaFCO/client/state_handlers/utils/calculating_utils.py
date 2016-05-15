#!/usr/bin/python3
from math import sqrt


def translate_coordinates(coordinates, cooficient):
    if coordinates is None:
        return
    return [(coordinate[0] / cooficient, coordinate[1] / cooficient) for coordinate in coordinates]


def calculate_scale(first_coordinates, second_coordinates):
    if first_coordinates is None or second_coordinates is None:
        return
    if len(first_coordinates) < 2 or len(second_coordinates) < 2:
        return
    cathetus_sqr1 = abs(first_coordinates[0][0] - first_coordinates[1][0]) ** 2
    cathetus_sqr2 = abs(first_coordinates[0][1] - first_coordinates[1][1]) ** 2
    first_line_length = sqrt(cathetus_sqr1 + cathetus_sqr2)
    cathetus_sqr1 = abs(second_coordinates[0][0] - second_coordinates[1][0]) ** 2
    cathetus_sqr2 = abs(second_coordinates[0][1] - second_coordinates[1][1]) ** 2
    second_line_length = sqrt(cathetus_sqr1 + cathetus_sqr2)

    return first_line_length / second_line_length

if __name__ == '__main__':
    pass
