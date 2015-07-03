import os

__author__ = 'Alexandr'


def string_to_matrix(string):
    matrix = []
    y_level = 0
    matrix.append([])  # Add empty cell to matrix
    for pix in string:
        if pix == "\n":
            y_level += 1
            matrix.append([])
        else:
            matrix[y_level].append(pix)
    return matrix


def read_matrix_from_file(file_path):
    stream = open(file_path)
    file_content = stream.read()
    frames_matrix_list = []
    for frame_string in file_content.split("# frame\n"):
        if len(frame_string) != 0:
            matrix_array = string_to_matrix(frame_string)
            last_element = matrix_array[len(matrix_array) - 1]
            if len(last_element) == 0:
                matrix_array.remove(last_element)
            frames_matrix_list.append(matrix_array)
    return frames_matrix_list[::-1]  # Reverse frames list


def print_matrix(matrix):
    for cell in matrix:
        print(cell)


def print_matrix_set(matrix_set):
    for matrix in matrix_set:
        print_matrix(matrix)


def clear_screen():
    pass
    # os.system("clear")  # linux
    os.system("cls")  # win


if __name__ == "__main__":
    demo_matrix_set = read_matrix_from_file("models/player_down.model")
    print_matrix_set(demo_matrix_set)
