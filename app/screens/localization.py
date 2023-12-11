from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextFieldRect

from misc.root import get_root


class LocalizationElement:
    def __init__(self, name: str, config_name: str | int, *args, **kwargs):
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

        if type(self.config_name) is str:
            for line in config_list:
                if self.config_name in line:
                    valuei = line.index('=') + 2
                    return line[valuei:-1]
        elif type(self.config_name) is int:
            for line in config_list:
                if "weekdays" in line:
                    valuei = line.index('=') + 3
                    weekdays = line[valuei:-2].split('", "')
                    return weekdays[self.config_name]

    def save_value(self):
        with open(get_root() + '/data/config.ini', encoding="UTF-8") as txtfile:
            config_list: list[str] = txtfile.readlines()

        config: str = ''
        if type(self.config_name) is str:
            for i, line in enumerate(config_list):
                if self.config_name in line:
                    valuei = line.index('=') + 2
                    config_list[i] = line[:valuei] + self.value_input.text + '\n'
                    break
            config = "".join(config_list)
        elif type(self.config_name) is int:
            for i, line in enumerate(config_list):
                if "weekdays" in line:
                    valuei = line.index('=') + 2
                    weekdays = line[valuei+1:-2].split('", "')
                    weekdays[self.config_name] = self.value_input.text
                    config_list[i] = line[:valuei] + '"' + '", "'.join(weekdays) + '"\n'
                    break
            config = "".join(config_list)

        with open(get_root() + '/data/config.ini', 'w', encoding="UTF-8") as txtfile:
            txtfile.write(config)


LOCALIZATION_ELS: list[LocalizationElement] = None


def save_values(*args, **kwargs):
    for time_config_el in LOCALIZATION_ELS:
        time_config_el.save_value()


def go_back_setup(*args, **kwargs):
    for time_config_el in LOCALIZATION_ELS:
        time_config_el.return_value_input_text()
    from app.screens.setup import current
    current("main")


class LocalizationScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        global LOCALIZATION_ELS
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

        LOCALIZATION_ELS = [
            LocalizationElement(
                name="Day",
                config_name="one_day"
            ),
            LocalizationElement(
                name="Few days",
                config_name="few_days"
            ),
            LocalizationElement(
                name="Many days",
                config_name="many_days"
            ),
            LocalizationElement(
                name="Hour",
                config_name="one_hour"
            ),
            LocalizationElement(
                name="Few hours",
                config_name="few_hours"
            ),
            LocalizationElement(
                name="Many hours",
                config_name="many_hours"
            ),
            LocalizationElement(
                name="Minute",
                config_name="one_minute"
            ),
            LocalizationElement(
                name="Few minutes",
                config_name="few_minutes"
            ),
            LocalizationElement(
                name="Many minutes",
                config_name="many_minutes"
            ),
            LocalizationElement(
                name="Will be in",
                config_name="will_be_in"
            ),
            LocalizationElement(
                name="Now",
                config_name="now"
            ),
            LocalizationElement(
                name="Good morning variants",
                config_name="good_morning"
            ),
            LocalizationElement(
                name="Monday",
                config_name=0
            ),
            LocalizationElement(
                name="Tuesday",
                config_name=1
            ),
            LocalizationElement(
                name="Wednesday",
                config_name=2
            ),
            LocalizationElement(
                name="Thursday",
                config_name=3
            ),
            LocalizationElement(
                name="Friday",
                config_name=4
            ),
            LocalizationElement(
                name="Saturday",
                config_name=5
            ),
            LocalizationElement(
                name="Sunday",
                config_name=6
            )
        ]

        for localization_el in LOCALIZATION_ELS:
            bl.height = bl.height + localization_el.size[1]
            bl.add_widget(localization_el.get_widget())

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
