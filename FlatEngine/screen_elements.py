from screen import *
from model_tools import generate_frames_from_string
__author__ = 'Alexandr'


class ScreenLabelModel(ScreenObjectModel):
    def __init__(self):
        super().__init__(frames_map=None, raw=False)
        self.text = ""

    def on_render(self):
        self.renderer_object.model_matrix_frames = generate_frames_from_string(self.text)
        # Update matrix by hands, skip lags
        self.renderer_object.model_matrix = self.renderer_object.model_matrix_frames[0]
        self.renderer_object.calculate_size()
        super().on_render()


class ScreenLabel(ScreenObject):
    def __init__(self, screen, update_text_func, text=""):
        self.text = text
        label_model = ScreenLabelModel()
        super().__init__(screen, label_model)
        self.update_text_func = update_text_func

    def update(self):
        self.model.text = str(self.update_text_func())
