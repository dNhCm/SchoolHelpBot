from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextFieldRect

from misc.root import get_root


class TimeConfigElement:
    def __init__(self, name: str, config_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config_name = config_name

        self.bl = MDBoxLayout(
            orientation='horizontal'
        )

        label = MDLabel(
            text=name,
            valign='middle'
        )
        label.font_size = 25
        label.bind(size=label.setter('text_size'))
        label.color = label.theme_cls.primary_color
        self.bl.add_widget(label)

        self.value_input = MDTextFieldRect(
            text=self.value_text()
        )

        self.bl.add_widget(self.value_input)

        self.size = (label.size[0]+self.value_input.size[0], label.size[1])

    def get_widget(self) -> Widget:
        return self.bl

    def return_value_input_text(self):
        self.value_input.text = self.value_text()

    def value_text(self) -> str:
        with open(get_root() + '/data/config.ini', encoding="UTF-8") as txtfile:
            config_list: list[str] = txtfile.readlines()

        for line in config_list:
            if self.config_name in line:
                valuei = line.index('=') + 2
                return line[valuei:-1]

    def save_value(self):
        with open(get_root() + '/data/config.ini', encoding="UTF-8") as txtfile:
            config_list: list[str] = txtfile.readlines()

        for i, line in enumerate(config_list):
            if self.config_name in line:
                valuei = line.index('=') + 2
                config_list[i] = line[:valuei] + self.value_input.text + '\n'
                break
        config = "".join(config_list)

        with open(get_root() + '/data/config.ini', 'w', encoding="UTF-8") as txtfile:
            txtfile.write(config)


TIME_CONFIG_ELS: list[TimeConfigElement] = None


def save_values(*args, **kwargs):
    for time_config_el in TIME_CONFIG_ELS:
        time_config_el.save_value()


def go_back_setup(*args, **kwargs):
    for time_config_el in TIME_CONFIG_ELS:
        time_config_el.return_value_input_text()
    from app.screens.setup import current
    current("main")


class TimeConfigScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        global TIME_CONFIG_ELS
        super().__init__(*args, **kwargs)

        label = MDLabel(
            text="Time Config Settings",
            halign='center',
            valign='top'
        )
        label.font_size = 70
        label.bind(size=label.setter('text_size'))
        label.color = label.theme_cls.primary_color
        self.add_widget(label)

        back_button = MDFillRoundFlatIconButton(
            text="Back",
            icon='keyboard-return',
            on_press=go_back_setup
        )
        back_button.pos_hint = {
            'y': 1 - back_button.size[1] / Window.size[1] - .01,
            'x': .01
        }
        self.add_widget(back_button)

        sv = MDScrollView(
            do_scroll_x=False,
            size_hint=(.6, .6),
            pos_hint={
                'center_x': .5,
                'y': .2
            }
        )
        bl = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=0
        )

        sv.add_widget(bl)

        TIME_CONFIG_ELS = [
            TimeConfigElement(
                name="Time zone",
                config_name="time_zone"
            ),
            TimeConfigElement(
                name="Advance time of messaging subject texts",
                config_name="subject_advance_time"
            ),
            TimeConfigElement(
                name="Delay after lesson started to deleting subject texts",
                config_name="deleting_subject_delay"
            )
        ]

        for time_config_el in TIME_CONFIG_ELS:
            bl.height = bl.height + time_config_el.size[1]
            bl.add_widget(time_config_el.get_widget())

        self.add_widget(sv)

        save_button = MDFillRoundFlatIconButton(
            text="Save",
            icon='content-save',
            size_hint=(.9, None),
            pos_hint={
                'center_x': .5,
                'y': .05
            },
            on_press=save_values
        )
        self.add_widget(save_button)
