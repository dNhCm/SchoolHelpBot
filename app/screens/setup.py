from kivy.clock import Clock
from kivy.graphics import Color
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager

from app.screens.localization import LocalizationScreen
from app.screens.subjects import SubjectsScreen
from app.screens.subjects_schedules import SubjectsSchedulesScreen
from app.screens.time_config import TimeConfigScreen
from app.screens.time_schedule import TimeScheduleScreen

# Global vars
CURRENT = "main"


def current(v: str = None) -> str:
    global CURRENT
    if v:
        CURRENT = v
    return CURRENT


class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        label = MDLabel(text="Setup", halign="center", valign="top")
        label.bind(size=label.setter('text_size'))
        label.font_size = 70
        label.color = Color(*label.theme_cls.primary_color).rgb
        self.add_widget(label)

        bl = MDBoxLayout(orientation="vertical", pos_hint={'x': .5 - .15, 'y': .5}, spacing=10)
        bl.add_widget(MDFillRoundFlatIconButton(text="Subjects", size_hint=(.3, None), icon="book-outline", on_press=go_subjects))
        bl.add_widget(MDFillRoundFlatIconButton(text="Time Schedule", size_hint=(.3, None), icon="clock-time-eight-outline", on_press=go_time_schedule))
        bl.add_widget(MDFillRoundFlatIconButton(text="Subjects Schedules", size_hint=(.3, None), icon="account-school-outline", on_press=go_subjects_schedules))
        bl.add_widget(MDFillRoundFlatIconButton(text="Localization", size_hint=(.3, None), icon="human-greeting-proximity", on_press=go_localization))
        bl.add_widget(MDFillRoundFlatIconButton(text="Time Config", size_hint=(.3, None), icon="camera-timer", on_press=go_time_config))

        self.add_widget(bl)


def go_subjects(*args, **kwargs):
    global CURRENT
    CURRENT = "subjects"


def go_time_schedule(*args, **kwargs):
    global CURRENT
    CURRENT = "time_schedule"


def go_subjects_schedules(*args, **kwargs):
    global CURRENT
    CURRENT = "subjects_schedules"


def go_localization(*args, **kwargs):
    global CURRENT
    CURRENT = "localization"


def go_time_config(*args, **kwargs):
    global CURRENT
    CURRENT = "time_config"


class SetupScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sm = MDScreenManager()

        self.sm.add_widget(MainScreen(name="main"))
        self.sm.add_widget(SubjectsScreen(name="subjects"))
        self.sm.add_widget(TimeScheduleScreen(name="time_schedule"))
        self.sm.add_widget(SubjectsSchedulesScreen(name="subjects_schedules"))
        self.sm.add_widget(LocalizationScreen(name="localization"))
        self.sm.add_widget(TimeConfigScreen(name="time_config"))

        self.add_widget(self.sm)

        self.update_sm_current()

    def update_sm_current(self, *args, **kwargs):
        if self.sm.current != CURRENT:
            self.sm.current = CURRENT
        Clock.schedule_once(self.update_sm_current)
