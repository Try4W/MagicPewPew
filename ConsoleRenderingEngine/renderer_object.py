__author__ = 'Alexandr'


class RendererObject(object):
    def __init__(self, pos_x=0, pos_y=0):
        self.model_matrix_frames = []  # Empty model matrix frames
        self.model_matrix_frame_counter = 0
        self.frame_rate = 5
        self.frame_rate_counter = 0
        self.reset_frame_rate_counter()
        self.model_matrix = []  # Empty model matrix
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = 0
        self.size_y = 0

    def calculate_size(self):
        self.size_y = len(self.model_matrix)
        self.size_x = 0
        for current_line in self.model_matrix:
            size_x_of_line = len(current_line)
            if self.size_x < size_x_of_line:
                self.size_x = size_x_of_line

    def update_animation_frame(self):
        self.model_matrix = self.model_matrix_frames[self.model_matrix_frame_counter]

    def update_frame_counter(self):
        if self.frame_rate_counter == 0:
            self.model_matrix_frame_counter -= 1  # Update frame counter
            self.reset_frame_rate_counter()
        if self.model_matrix_frame_counter < 0:
            self.reset_animation_frame_counter()
        self.frame_rate_counter -= 1  # Update frame rate counter

    def reset_frame_rate_counter(self):
        self.frame_rate_counter = self.frame_rate

    def reset_animation_frame_counter(self):
        self.model_matrix_frame_counter = len(self.model_matrix_frames) - 1

    def on_render(self):
        self.update_animation_frame()
        self.calculate_size()
        if len(self.model_matrix_frames) > 0:
            self.update_frame_counter()

    def set_model_matrix_frames(self, model_matrix_frames):
        self.model_matrix_frames = model_matrix_frames
        self.reset_animation_frame_counter()
