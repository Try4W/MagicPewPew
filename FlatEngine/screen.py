import sys

sys.path.insert(0, '../ConsoleRenderingEngine/')

from rendering import Renderer
from renderer_object import RendererObject
from tools import read_matrix_from_file
from tools import clear_screen
from threading import Thread
import time


class ScreenRendererUpdater(Thread):
    def __init__(self, renderer_obj, world_obj):
        super().__init__()
        self.renderer_obj = renderer_obj
        self.allow_rendering = True
        self.screen_obj = world_obj

    def run(self):
        while self.allow_rendering:
            if not self.renderer_obj.debug_mode:
                clear_screen()
            # Clear screen objects list
            self.renderer_obj.renderer_objects.clear()
            for screen_object in self.screen_obj.screen_objects:
                screen_object.model.on_render()
                renderer_obj = screen_object.model.get_renderer_object()
                renderer_obj.pos_x = screen_object.pos_x
                renderer_obj.pos_y = self.renderer_obj.screen_y - (renderer_obj.size_y + screen_object.pos_y)
                self.renderer_obj.renderer_objects.append(renderer_obj)
                # print("Obj: x/y: " + str(screen_object.pos_x) + "/" + str(screen_object.pos_y))
                # print(" @ renderer-Obj: x/y: " + str(renderer_obj.pos_x) + "/" + str(renderer_obj.pos_y))
                # print(" @ renderer-Obj: size(x/y): " + str(renderer_obj.size_x) + "/" + str(renderer_obj.size_y))

            self.renderer_obj.clear_screen_buffer()
            self.renderer_obj.print_renderer_objects_to_matrix()
            self.renderer_obj.render()
            # print("Objects in renderer: " + str(len(self.renderer_obj.renderer_objects)))
            # print("Objects in world: " + str(len(self.world_obj.screen_objects)))


class ScreenUpdater(Thread):
    def __init__(self, world):
        super().__init__()
        self.setName("WorldUpdater")
        self.world = world
        self.allow_updating = True

    def run(self):
        while self.allow_updating:
            self.world.update()
            time.sleep(0.1)


class Screen(object):
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.screen_objects = []

        # Set renderer updater
        self.screen_renderer = Renderer(size_x, size_y)
        self.screen_renderer_updater = ScreenRendererUpdater(self.screen_renderer, self)
        self.screen_renderer_updater.start()

        # Set world updater (objects ticks)
        self.screen_updater = ScreenUpdater(self)
        self.screen_updater.start()

    def update(self):
        for screen_object in self.screen_objects:
            screen_object.update()

    def add_object(self, world_object):
        self.screen_objects.append(world_object)

    def destroy(self):
        self.screen_renderer_updater.allow_rendering = False
        self.screen_updater.allow_updating = False
        clear_screen()


class ScreenObject(object):
    def __init__(self, screen, model, pos_x=0, pos_y=0):
        self.screen = screen
        self.model = model
        self.model.parent_screen_object = self
        self.pos_x = pos_x
        self.pos_y = pos_y

    def update(self):
        # update things
        pass


class ScreenObjectModel(object):
    def __init__(self, frames_map, raw=True):
        if raw:
            for frames_tag, frames_path in frames_map.items():
                # Convert paths in matrix set
                frames_map[frames_tag] = read_matrix_from_file(frames_path)
        self.frames_map = frames_map
        self.renderer_object = RendererObject()
        self.center_hor = False
        self.parent_screen_object = None

    def on_render(self):
        if self.center_hor:
            self.parent_screen_object.pos_x = int(
                (self.parent_screen_object.screen.size_x / 2) - (self.renderer_object.size_x / 2))

    def set_current_frames(self, key):
        self.renderer_object.model_matrix_frames = self.frames_map[key]
        self.renderer_object.reset_animation_frame_counter()

    def get_renderer_object(self):
        return self.renderer_object


if __name__ == "__main__":
    demo_screen = Screen(50, 20)

    # Read demo object model
    demo_frames_map = {"FLY_RIGHT": "../ConsoleRenderingEngine/models/example_right.model",
                       "FLY_LEFT": "../ConsoleRenderingEngine/models/example_left.model"}
    demo_monster_model = ScreenObjectModel(demo_frames_map)
    demo_monster_model.set_current_frames("FLY_RIGHT")

    # Add object in world
    demo_monster = ScreenObject(demo_screen, demo_monster_model)
    demo_screen.add_object(demo_monster)
    demo_monster.pos_x = 5
    demo_monster.pos_y = 3
