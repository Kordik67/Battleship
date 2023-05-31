from ursina import Entity, Slider, Audio, Func
from .MenuButton import MenuButton

class OptionsMenu(Entity):
    def __init__(self, parent, background_music, state_handler, button_spacing):
        super().__init__(parent=parent)

        # Volume
        self.volume_slider = Slider(0, 1, default=Audio.volume_multiplier, step=.1, text="Volume :", parent=self, x=-.25)
        self.volume_slider.on_value_changed = lambda:self.set_volume_multiplier(background_music)

        # Back button
        self.back_button = MenuButton(parent=self, text="Retour", x=-.25, origin_x=-.5, on_click=Func(setattr, state_handler, 'state', 'main_menu'))

        for i, e in enumerate((self.volume_slider, self.back_button)):
            e.y = -i * button_spacing

    def set_volume_multiplier(self, sound):
        sound.volume = self.volume_slider.value