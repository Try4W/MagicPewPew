import sys
sys.path.insert(0, '../ConsoleRenderingEngine/')

from tools import read_matrix_from_file
from tools import string_to_matrix

__author__ = 'Alexandr'


def load_frames(path_to_file):
    return read_matrix_from_file(path_to_file)


def generate_frames_from_string(string):
    matrix = string_to_matrix(string)
    return [matrix]

if __name__ == "__main__":
    from tools import print_matrix_set
    demo_generated_frames = generate_frames_from_string("Test string \n"
                                                        "Second line of test string!")
    print_matrix_set(demo_generated_frames)
