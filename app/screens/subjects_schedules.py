
import json
import os

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatIconButton, MDRectangleFlatButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField

from misc.root import get_root


CURRENT: str = "main"
NEED_UPDATE: bool = False


def go_back(*args):
    global CURRENT, NEED_UPDATE
    NEED_UPDATE = True
    CURRENT = "main"


class SubjectElement:
    def __init__(self):
        ...


class WeekElement:
    def __init__(self, week: str, weekdays_subjects: list[list[str]]):
        self.week = week
        self.height = 0

        self.widgets = self.build_widget(weekdays_subjects)

    def delete_weekday(self, weekday_i: int):
        global NEED_UPDATE

        with open(get_root() + "/data/subjects_schedules/schedules.json", encoding="UTF-8") as jsonfile:
            subjects_schedules: dict[str: list[list[str]]] = json.load(jsonfile)

        subjects_schedules[self.week].pop(weekday_i)

        with open(get_root() + "/data/subjects_schedules/schedules.json", 'w', encoding="UTF-8") as jsonfile:
            json.dump(subjects_schedules, jsonfile)

        NEED_UPDATE = True

    def weekday_delete_popup(self, transform: tuple, weekday_i: int, *args):
        if not (
                transform[0] <= args[0].x <= transform[0] + transform[2]
                and transform[1] <= args[0].y <= transform[1] + transform[3]
        ):
            return

        content = MDFloatLayout()

        cancel_button = MDFillRoundFlatIconButton(
            text="Cancel",
            icon="cancel",
            size_hint=(.9 / 2 - .05 / 2, None),
            pos_hint={
                'center_y': .5,
                'x': .05
            }
        )
        cancel_button.md_bg_color = cancel_button.theme_cls.disabled_primary_color
        content.add_widget(cancel_button)

        delete_button = MDFillRoundFlatIconButton(
            text="Delete",
            icon="delete",
            size_hint=(.9 / 2 - .05 / 2, None),
            pos_hint={
                'center_y': .5,
                'x': 1 - .05 - .9 / 2 + .05 / 2
            }
        )
        delete_button.md_bg_color = cancel_button.theme_cls.error_color
        content.add_widget(delete_button)

        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        popup = Popup(
            title=f"Delete {weekdays[weekday_i]} of the {self.week} week",
            content=content
        )
        cancel_button.bind(on_press=popup.dismiss)

        def on_press_delete_btn(*args):
            self.delete_weekday(weekday_i)
            popup.dismiss()

        delete_button.bind(on_press=on_press_delete_btn)

        popup.open()

    def delete_week(self):
        global NEED_UPDATE

        with open(get_root() + "/data/subjects_schedules/schedules.json", encoding="UTF-8") as jsonfile:
            subjects_schedules: dict[str: list[list[str]]] = json.load(jsonfile)

        del subjects_schedules[self.week]

        with open(get_root() + "/data/subjects_schedules/schedules.json", 'w', encoding="UTF-8") as jsonfile:
            json.dump(subjects_schedules, jsonfile)

        NEED_UPDATE = True

    def week_delete_popup(self, transform: tuple, *args):
        if not (
            transform[0] <= args[0].x <= transform[0] + transform[2]
            and transform[1] <= args[0].y <= transform[1] + transform[3]
        ):
            return

        content = MDFloatLayout()

        cancel_button = MDFillRoundFlatIconButton(
            text="Cancel",
            icon="cancel",
            size_hint=(.9 / 2 - .05 / 2, None),
            pos_hint={
                'center_y': .5,
                'x': .05
            }
        )
        cancel_button.md_bg_color = cancel_button.theme_cls.disabled_primary_color
        content.add_widget(cancel_button)

        delete_button = MDFillRoundFlatIconButton(
            text="Delete",
            icon="delete",
            size_hint=(.9 / 2 - .05 / 2, None),
            pos_hint={
                'center_y': .5,
                'x': 1 - .05 - .9 / 2 + .05 / 2
            }
        )
        delete_button.md_bg_color = cancel_button.theme_cls.error_color
        content.add_widget(delete_button)

        popup = Popup(
            title=f"Delete {self.week}",
            content=content
        )
        cancel_button.bind(on_press=popup.dismiss)

        def on_press_delete_btn(*args):
            self.delete_week()
            popup.dismiss()

        delete_button.bind(on_press=on_press_delete_btn)

        popup.open()

    def delete_subject(self, weekday_i: int, i: int):
        global NEED_UPDATE

        with open(get_root() + "/data/subjects_schedules/schedules.json", encoding="UTF-8") as jsonfile:
            subjects_schedules: dict[str: list[list[str]]] = json.load(jsonfile)

        subjects_schedules[self.week][weekday_i].pop(i)

        with open(get_root() + "/data/subjects_schedules/schedules.json", 'w', encoding="UTF-8") as jsonfile:
            json.dump(subjects_schedules, jsonfile)

        NEED_UPDATE = True

    def build_widget(self, weekdays_subjects: list[list[str]]) -> list[Widget]:
        widgets = []

        week_label = MDLabel(
            text=self.week,
            size_hint=(None, None)
        )
        week_label.font_size = 35
        week_label.bind(size=week_label.setter('text_size'))
        week_label.color = week_label.theme_cls.primary_color
        week_label.texture_update()
        week_label.size = week_label.texture_size
        week_label.on_touch_down = lambda x: self.week_delete_popup((*week_label.pos, *week_label.size), x)
        widgets.append(week_label)
        self.height += week_label.size[1]

        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for weekday, subjects in zip(weekdays, weekdays_subjects):
            weekday_i = weekdays.index(weekday)

            match weekday_i:
                case 0:
                    weekday_label0 = MDLabel(
                        text=weekday,
                        size_hint=(None, None)
                    )
                    weekday_label0.font_size = 25
                    weekday_label0.bind(size=weekday_label0.setter('text_size'))
                    weekday_label0.color = weekday_label0.theme_cls.primary_color
                    weekday_label0.texture_update()
                    weekday_label0.size = weekday_label0.texture_size
                    weekday_label0.on_touch_down = lambda x: self.weekday_delete_popup(
                        (*weekday_label0.pos, *weekday_label0.size),
                        0,
                        x
                    )
                    widgets.append(weekday_label0)
                    self.height += weekday_label0.size[1]
                case 1:
                    weekday_label1 = MDLabel(
                        text=weekday,
                        size_hint=(None, None)
                    )
                    weekday_label1.font_size = 25
                    weekday_label1.bind(size=weekday_label1.setter('text_size'))
                    weekday_label1.color = weekday_label1.theme_cls.primary_color
                    weekday_label1.texture_update()
                    weekday_label1.size = weekday_label1.texture_size
                    weekday_label1.on_touch_down = lambda x: self.weekday_delete_popup(
                        (*weekday_label1.pos, *weekday_label1.size),
                        1,
                        x
                    )
                    widgets.append(weekday_label1)
                    self.height += weekday_label1.size[1]
                case 2:
                    weekday_label2 = MDLabel(
                        text=weekday,
                        size_hint=(None, None)
                    )
                    weekday_label2.font_size = 25
                    weekday_label2.bind(size=weekday_label2.setter('text_size'))
                    weekday_label2.color = weekday_label2.theme_cls.primary_color
                    weekday_label2.texture_update()
                    weekday_label2.size = weekday_label2.texture_size
                    weekday_label2.on_touch_down = lambda x: self.weekday_delete_popup(
                        (*weekday_label2.pos, *weekday_label2.size),
                        2,
                        x
                    )
                    widgets.append(weekday_label2)
                    self.height += weekday_label2.size[1]
                case 3:
                    weekday_label3 = MDLabel(
                        text=weekday,
                        size_hint=(None, None)
                    )
                    weekday_label3.font_size = 25
                    weekday_label3.bind(size=weekday_label3.setter('text_size'))
                    weekday_label3.color = weekday_label3.theme_cls.primary_color
                    weekday_label3.texture_update()
                    weekday_label3.size = weekday_label3.texture_size
                    weekday_label3.on_touch_down = lambda x: self.weekday_delete_popup(
                        (*weekday_label3.pos, *weekday_label3.size),
                        3,
                        x
                    )
                    widgets.append(weekday_label3)
                    self.height += weekday_label3.size[1]
                case 4:
                    weekday_label4 = MDLabel(
                        text=weekday,
                        size_hint=(None, None)
                    )
                    weekday_label4.font_size = 25
                    weekday_label4.bind(size=weekday_label4.setter('text_size'))
                    weekday_label4.color = weekday_label4.theme_cls.primary_color
                    weekday_label4.texture_update()
                    weekday_label4.size = weekday_label4.texture_size
                    weekday_label4.on_touch_down = lambda x: self.weekday_delete_popup(
                        (*weekday_label4.pos, *weekday_label4.size),
                        4,
                        x
                    )
                    widgets.append(weekday_label4)
                    self.height += weekday_label4.size[1]
                case 5:
                    weekday_label5 = MDLabel(
                        text=weekday,
                        size_hint=(None, None)
                    )
                    weekday_label5.font_size = 25
                    weekday_label5.bind(size=weekday_label5.setter('text_size'))
                    weekday_label5.color = weekday_label5.theme_cls.primary_color
                    weekday_label5.texture_update()
                    weekday_label5.size = weekday_label5.texture_size
                    weekday_label5.on_touch_down = lambda x: self.weekday_delete_popup(
                        (*weekday_label5.pos, *weekday_label5.size),
                        5,
                        x
                    )
                    widgets.append(weekday_label5)
                    self.height += weekday_label5.size[1]
                case 6:
                    weekday_label6 = MDLabel(
                        text=weekday,
                        size_hint=(None, None)
                    )
                    weekday_label6.font_size = 25
                    weekday_label6.bind(size=weekday_label6.setter('text_size'))
                    weekday_label6.color = weekday_label6.theme_cls.primary_color
                    weekday_label6.texture_update()
                    weekday_label6.size = weekday_label6.texture_size
                    weekday_label6.on_touch_down = lambda x: self.weekday_delete_popup(
                        (*weekday_label6.pos, *weekday_label6.size),
                        6,
                        x
                    )
                    widgets.append(weekday_label6)
                    self.height += weekday_label6.size[1]

            for i, subject in enumerate(subjects):
                subject_button = MDRectangleFlatButton(
                    text="      " + subject,
                    pos_hint={"x": .04},
                    on_press=lambda x, y=weekday_i, z=i: self.delete_subject(y, z)
                )
                widgets.append(subject_button)
                self.height += subject_button.size[1]

        return widgets

    def get_widget(self) -> MDBoxLayout:
        return self.widgets


class AddWeekScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        label = MDLabel(
            text="Add Week",
            halign='center',
            valign='top'
        )
        label.font_size = 70
        label.bind(size=label.setter('text_size'))
        label.color = label.theme_cls.primary_color
        self.add_widget(label)

        week_name_input = MDTextField(
            mode="fill",
            hint_text='Week name',
            helper_text='Input any week name like (A, B, C ...)',
            required=True,
            size_hint=(0.9, None),
            pos_hint={
                'center_x': .5,
                'center_y': .5
            }
        )

        def create_new_week(*args):
            with open(get_root() + "/data/subjects_schedules/schedules.json", encoding="UTF-8") as jsonfile:
                subjects_schedules: dict[str: list[list[str]]] = json.load(jsonfile)

            if week_name_input.text in subjects_schedules.keys():
                return

            subjects_schedules[week_name_input.text] = [
                ["none"],
                ["none"],
                ["none"],
                ["none"],
                ["none"],
                ["none"],
                ["none"]
            ]

            with open(get_root() + "/data/subjects_schedules/schedules.json", 'w', encoding="UTF-8") as jsonfile:
                json.dump(subjects_schedules, jsonfile)

            go_back()
            week_name_input.text = ''

        week_name_input.bind(on_text_validate=create_new_week)
        self.add_widget(week_name_input)

        cancel_button = MDFillRoundFlatIconButton(
            text="Cancel",
            icon="cancel",
            size_hint=(.9, None),
            pos_hint={
                'y': .03,
                'center_x': .5
            },
            on_press=go_back
        )
        cancel_button.md_bg_color = cancel_button.theme_cls.disabled_primary_color
        self.add_widget(cancel_button)


class AddSubjectScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        label = MDLabel(
            text="Add subject",
            halign='center',
            valign='top'
        )
        label.font_size = 70
        label.bind(size=label.setter('text_size'))
        label.color = label.theme_cls.primary_color
        self.add_widget(label)

        bl = MDBoxLayout(
            orientation="vertical",
            pos_hint={
                'y': .2
            },
            spacing=20
        )
        self.add_widget(bl)

        self.subject_choice = MDRectangleFlatButton(
            text="Choose subject: none",
            size_hint=(.4, None),
            pos_hint={
                'center_x': .5
            },
            on_press=self.open_subjects_lbs
        )
        self.subject_choice.subject = "none"
        bl.add_widget(self.subject_choice)

        self.week_choice = MDRectangleFlatButton(
            text=f"Choose week: {list(self.get_subjects_schedules().keys())[0]}",
            size_hint=(.4, None),
            pos_hint={
                'center_x': .5
            },
            on_press=self.open_week_lbs
        )
        self.week_choice.week = list(self.get_subjects_schedules().keys())[0]
        bl.add_widget(self.week_choice)

        self.weekday_choice = MDRectangleFlatButton(
            text="Choose weekday: Monday",
            size_hint=(.4, None),
            pos_hint={
                'center_x': .5
            },
            on_press=self.open_weekday_lbs
        )
        self.weekday_choice.weekday_i = 0
        bl.add_widget(self.weekday_choice)

        self.subject_i_input = MDTextField(
            mode="rectangle",
            hint_text="Index of subject",
            helper_text="Input number (0, 1, 2, -1 ...)",
            text="-1",
            size_hint=(.4, None),
            pos_hint={
                'center_x': .5
            },
            on_text_validate=self.on_subject_i_text_validate
        )
        self.subject_i_input.subject_i = -1
        bl.add_widget(self.subject_i_input)

        cancel_button = MDFillRoundFlatIconButton(
            text="Cancel",
            icon="cancel",
            size_hint=(.9 / 2 - .05 / 2, None),
            pos_hint={
                'y': .03,
                'x': .05
            },
            on_press=self.go_back
        )
        cancel_button.md_bg_color = cancel_button.theme_cls.disabled_primary_color
        self.add_widget(cancel_button)

        add_button = MDFillRoundFlatIconButton(
            text="Add",
            icon="card-plus",
            size_hint=(.9 / 2 - .05 / 2, None),
            pos_hint={
                'y': .03,
                'x': 1 - .05 - .9 / 2 + .05 / 2
            },
            on_press=self.add_subject
        )
        self.add_widget(add_button)

    def go_back(self, *args):
        go_back()
        self.subject_choice.text = 'Choose subject: none'
        self.subject_choice.subject = 'none'
        self.subject_i_input.text = "-1"
        self.subject_i_input.subject_i = -1

    def add_subject(self, *args):
        subjects_schedules = self.get_subjects_schedules()

        subjects_schedules[self.week_choice.week][self.weekday_choice.weekday_i].insert(self.subject_i_input.subject_i, self.subject_choice.subject)

        with open(get_root() + "/data/subjects_schedules/schedules.json", 'w', encoding="UTF-8") as jsonfile:
            json.dump(subjects_schedules, jsonfile)

        self.go_back()

    @staticmethod
    def get_subjects() -> dict[str: str]:
        subjects = [subject[:-4] for subject in os.listdir(get_root() + '/data/subjects/')]

        formatted_subjects: dict[str] = dict()
        for subject in subjects:
            with open(get_root() + f'/data/subjects/{subject}.txt', encoding="UTF-8") as txtfile:
                formatted_subjects[subject] = txtfile.read()

        return formatted_subjects

    def subject_lbs_callback(self, subject: str):
        self.subject_choice.text = f"Subject: {subject}"
        self.subject_choice.subject = subject

    def open_subjects_lbs(self, *args):
        lbs = MDListBottomSheet()
        for subject in self.get_subjects().keys():
            lbs.add_item(
                text=subject,
                callback=lambda x, y=subject: self.subject_lbs_callback(y)
            )
        lbs.open()

    @staticmethod
    def get_subjects_schedules() -> dict[str: list[list[str]]]:
        with open(get_root()+'/data/subjects_schedules/schedules.json', encoding="UTF-8") as jsonfile:
            return json.load(jsonfile)

    def week_lbs_callback(self, week: str):
        self.week_choice.text = f"Week: {week}"
        self.week_choice.week = week

    def open_week_lbs(self, *args):
        lbs = MDListBottomSheet()
        for week in self.get_subjects_schedules().keys():
            lbs.add_item(
                text=week,
                callback=lambda x, y=week: self.week_lbs_callback(y)
            )
        lbs.open()

    def weekday_lbs_callback(self, weekday: str):
        self.weekday_choice.text = f"Weekday: {weekday}"
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.weekday_choice.weekday_i = weekdays.index(weekday)

    def open_weekday_lbs(self, *args):
        lbs = MDListBottomSheet()
        for weekday in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            lbs.add_item(
                text=weekday,
                callback=lambda x, y=weekday: self.weekday_lbs_callback(y)
            )
        lbs.open()

    def on_subject_i_text_validate(self, *args):
        try:
            self.subject_i_input.subject_i = int(self.subject_i_input.text)
        except TypeError:
            self.subject_i_input.text = "-1"
            self.subject_i_input.subject_i = -1


def go_back_setup(*args, **kwargs):
    from app.screens.setup import current
    current("main")


class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        label = MDLabel(
            text="Subjects Schedules Settings",
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

        self.sv = MDScrollView(
            do_scroll_x=False,
            size_hint=(.7, .6),
            pos_hint={
                'center_x': .5,
                'y': .1
            }
        )
        self.weeks_bl: MDBoxLayout = None
        self.add_widget(self.sv)

        def on_add_week_btn_press(*args):
            global CURRENT
            CURRENT = "add_week"

        add_week_btn = MDFillRoundFlatIconButton(
            text="Add week",
            icon="calendar-week",
            size_hint=(.9 / 2 - .05 / 2, None),
            pos_hint={
                'y': .03,
                'x': .05
            },
            on_press=on_add_week_btn_press
        )
        self.add_widget(add_week_btn)

        def on_add_subject_btn_press(*args):
            global CURRENT
            CURRENT = "add_subject"

        add_subject_btn = MDFillRoundFlatIconButton(
            text="Add subject",
            icon="book-plus",
            size_hint=(.9 / 2 - .05 / 2, None),
            pos_hint={
                'y': .03,
                'x': 1 - .05 - .9 / 2 + .05 / 2
            },
            on_press=on_add_subject_btn_press
        )
        self.add_widget(add_subject_btn)

        self.update_canvas()
        self.check_need_update()

    @staticmethod
    def get_subjects_schedules() -> dict[str: list[list[str]]]:
        with open(get_root() + '/data/subjects_schedules/schedules.json', encoding="UTF-8") as jsonfile:
            return json.load(jsonfile)

    def update_canvas(self):
        self.remove_widget(self.sv)

        self.sv = MDScrollView(
            do_scroll_x=False,
            size_hint=(.7, .6),
            pos_hint={
                'center_x': .5,
                'y': .1
            },
            scroll_y=self.sv.scroll_y
        )

        self.weeks_bl = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=.01 * Window.size[1],
            height=0
        )
        self.sv.add_widget(self.weeks_bl)

        subjects_schedules = self.get_subjects_schedules()
        for k, v in subjects_schedules.items():
            week = WeekElement(
                week=k,
                weekdays_subjects=v
            )
            for widget in week.get_widget():
                self.weeks_bl.add_widget(widget)
            self.weeks_bl.height = self.weeks_bl.height + week.height + (len(week.get_widget()) - 1) * .01 * Window.size[1]

        self.add_widget(self.sv)

    def check_need_update(self, *args, **kwargs):
        global NEED_UPDATE
        if NEED_UPDATE:
            self.update_canvas()
            NEED_UPDATE = False
        Clock.schedule_once(self.check_need_update)


class SubjectsSchedulesScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sm = MDScreenManager()

        self.sm.add_widget(MainScreen(name="main"))
        self.sm.add_widget(AddWeekScreen(name="add_week"))
        self.sm.add_widget(AddSubjectScreen(name="add_subject"))

        self.add_widget(self.sm)

        self.update_current()

    def update_current(self, *args, **kwargs):
        self.sm.current = CURRENT
        Clock.schedule_once(self.update_current)
