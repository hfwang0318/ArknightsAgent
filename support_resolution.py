import operator


def get_support_resolution():
    resolution_lists = [[1600, 900]]
    return resolution_lists


def is_valid(resolution):
    resolution_lists = get_support_resolution()
    for valid_resolution in resolution_lists:
        if operator.eq(resolution, valid_resolution):
            __is_valid = True

    if not __is_valid:
        raise Exception('not support resolution with {} * {}'.format(resolution[0], resolution[1]))