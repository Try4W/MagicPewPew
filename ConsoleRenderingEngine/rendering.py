from renderer_object import RendererObject
from tools import read_matrix_from_file
from tools import clear_screen
from threading import Thread
import time

__author__ = 'Alexandr'


class Renderer(object):
    def __init__(self, screen_x=100, screen_y=3, frame_timeout=0.0):
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.last_fps_time = 0
        self.fps = 0
        self.fps_tmp = 0
        self.frame_timeout = frame_timeout

        self.screen_matrix = []  # y - arrays, x - string
        self.renderer_objects = []

        self.debug_mode = False

    def clear_screen_buffer(self):
        self.screen_matrix.clear()  # Clear buffer
        for y_parser in range(self.screen_y):
            self.screen_matrix.append([])
            line_array = self.screen_matrix[y_parser]
            # Create empty matrix
            for x_parser in range(self.screen_x):
                line_array.append([" "])

    def print_renderer_objects_to_matrix(self):
        for obj in self.renderer_objects:
            obj.on_render()
            draw_pos_y = obj.pos_y

            for lvl_array in obj.model_matrix:
                draw_pos_x = obj.pos_x
                for line_array in lvl_array:
                    if (draw_pos_x < self.screen_x and draw_pos_y < self.screen_y)\
                            and (draw_pos_x >= 0 and draw_pos_y >= 0):  # Check is part on the screen
                        if self.screen_matrix[draw_pos_y][draw_pos_x][0] == " ":
                            self.screen_matrix[draw_pos_y][draw_pos_x] = line_array[0]
                        else:
                            self.screen_matrix[draw_pos_y][draw_pos_x] = ["█"]
                    draw_pos_x += 1
                draw_pos_y += 1

    def render(self):
        # FPS counter
        self.fps_tmp += 1
        current_time = time.time()
        if current_time > self.last_fps_time + 1:
            self.last_fps_time = current_time
            self.fps = self.fps_tmp
            self.fps_tmp = 0

        # Render things
        self.draw_line()
        # counter = 0
        for lvl_array in self.screen_matrix:
            # counter += 1
            # print(str(counter), end="")
            for line_array in lvl_array:
                try:
                    print(line_array[0], end='')
                except UnicodeEncodeError:
                    print("~", end='')
            print()  # Move to next line
        self.draw_line()
        time.sleep(self.frame_timeout)
        if self.debug_mode:
            time.sleep(2.5)
            print("One more time...")
            time.sleep(2.5)

    def draw_line(self):
        print("#", end="")
        for drawer in range(self.screen_x):
            print("-", end="")
        print("#")

    def update_screen(self):
        self.screen_matrix.clear()


if __name__ == "__main__":
    frames_matrix_go_right = read_matrix_from_file("models/example_right.model")
    frames_matrix_go_left = read_matrix_from_file("models/example_left.model")

    renderer = Renderer()

    demo_object = RendererObject(0, 0)
    renderer.renderer_objects.append(demo_object)
    go_right = True
    while True:
        # Walk logic
        if demo_object.pos_x == 0:
            go_right = True
            demo_object.set_model_matrix_frames(frames_matrix_go_right)
        if demo_object.pos_x == renderer.screen_x - 19:
            go_right = False
            demo_object.set_model_matrix_frames(frames_matrix_go_left)

        if go_right:
            demo_object.pos_x += 1
        else:  # go left
            demo_object.pos_x -= 1

        renderer.clear_screen_buffer()
        clear_screen()
        renderer.print_renderer_objects_to_matrix()
        renderer.render()
        # input("Monster at " + str(demo_object.pos_x) + "; Press smt for next frame")
