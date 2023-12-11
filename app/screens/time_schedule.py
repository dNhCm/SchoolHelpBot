import json

from kivy.clock import Clock
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDFillRoundFlatIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField

from misc.root import get_root

# Global vars
NEED_UPDATE: bool = False


# Public funcs
def add_time(time: str):
    with open(get_root() + '/data/time_schedule/schedule.json', encoding='UTF-8') as jsonfile:
        time_schedule: list[str] = json.load(jsonfile)

    if time_schedule:
        sum_min = lambda h, m: h * 60 + m
        time_schedule_min = [sum_min(*list(map(int, time.split(':')))) for time in time_schedule]
        time_min = sum_min(*list(map(int, time.split(':'))))

        for i, schedule_time_min in enumerate(time_schedule_min):
            if time_min <= schedule_time_min:
                time_schedule.insert(i, time)
                break
        else:
            time_schedule.append(time)
    else:
        time_schedule = [time]

    with open(get_root() + '/data/time_schedule/schedule.json', 'w', encoding='UTF-8') as jsonfile:
        json.dump(time_schedule, jsonfile)


class TimeButton(MDRectangleFlatButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pos_hint = {
            'center_x': .5
        }

    def on_press(self):
        global NEED_UPDATE
        with open(get_root() + '/data/time_schedule/schedule.json', encoding='UTF-8') as jsonfile:
            time_schedule: list[str] = json.load(jsonfile)

        time_schedule.remove(self.text)

        with open(get_root() + '/data/time_schedule/schedule.json', 'w', encoding='UTF-8') as jsonfile:
            json.dump(time_schedule, jsonfile)

        NEED_UPDATE = True


class AddTimeInput(MDTextField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mode = 'fill'
        self.helper_text_mode = 'on_focus'
        self.hint_text = 'Enter time to add'
        self.helper_text = 'Format it by HH:mm'
        self.max_text_length = 5
        self.size_hint = (.6, None)
        self.pos_hint = {
            'center_x': .5,
            'y': .03
        }

    def on_text_validate(self):
        global NEED_UPDATE
        add_time(self.text)
        NEED_UPDATE = True


def go_back_setup(*args, **kwargs):
    from app.screens.setup import current
    current("main")


class TimeScheduleScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        label = MDLabel(
            text="Time Schedule Settings",
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

        self.add_widget(AddTimeInput())

        self.sv = MDScrollView(
            do_scroll_x=False,
            size_hint=(.6, .7),
            pos_hint={
                'center_x': .5,
                'y': .1
            }
        )

        self.bl = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=0
        )

        self.sv.add_widget(self.bl)
        self.add_widget(self.sv)

        self.update_canvas()
        self.check_need_update()

    def update_canvas(self):
        self.remove_widget(self.sv)

        self.sv = MDScrollView(
            do_scroll_x=False,
            size_hint=(.6, .7),
            pos_hint={
                'center_x': .5,
                'y': .1
            }
        )

        self.bl = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=0
        )

        self.sv.add_widget(self.bl)
        self.add_widget(self.sv)

        with open(get_root() + '/data/time_schedule/schedule.json', encoding='UTF-8') as jsonfile:
            time_schedule: list[str] = json.load(jsonfile)

        for time in time_schedule:
            button = TimeButton(
                text=time
            )
            self.bl.add_widget(button)
            self.bl.height = self.bl.height + button.size[1]

    def check_need_update(self, *args, **kwargs):
        global NEED_UPDATE
        if NEED_UPDATE:
            self.update_canvas()
            NEED_UPDATE = False
        Clock.schedule_once(self.check_need_update)
