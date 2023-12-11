import os
from time import sleep

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.uix.popup import Popup
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDFillRoundFlatIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField

from misc.root import get_root


def go_back(*args, **kwargs):
    SubjectsUpdater.current_sm("main")
    SubjectsUpdater.need_update(True)


class SubjectScreenTemplate(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        label = MDLabel(
            text=self.name + " subject",
            halign='center',
            valign='top'
        )
        label.font_size = 70
        label.bind(size=label.setter('text_size'))
        label.color = label.theme_cls.primary_color
        self.add_widget(label)

        with open(get_root() + f'/data/subjects/{self.name}.txt', encoding="UTF-8") as txtfile:
            text: str = txtfile.read()

        self.text_input = MDTextField(
            mode="fill",
            text='\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'+text,
            hint_text='Edit subject text',
            helper_text='Every new line is another message',
            required=True,
            multiline=True,
            size_hint=(0.9, .5),
            max_height=Window.size[1] * .6,
            pos_hint={
                'center_x': .5,
                'y': .2
            }
        )
        self.text_input.line_color_normal = self.text_input.theme_cls.primary_color
        self.text_input.hint_text_color_normal = self.text_input.theme_cls.primary_color
        self.text_input.line_color_focus = self.text_input.theme_cls.accent_color
        self.add_widget(self.text_input)

        cancel_button = MDFillRoundFlatIconButton(
            text="Cancel",
            icon="cancel",
            size_hint=(.9 / 3 - .05 / 2, None),
            pos_hint={
                'y': .03,
                'x': .05
            },
            on_press=self.go_back
        )
        cancel_button.md_bg_color = cancel_button.theme_cls.disabled_primary_color
        self.add_widget(cancel_button)

        save_button = MDFillRoundFlatIconButton(
            text="Save",
            icon="content-save-edit",
            size_hint=(.9 / 3 - .05 / 2, None),
            pos_hint={
                'y': .03,
                'x': 0.075 + .9 / 3
            },
            on_press=self.save_edit
        )
        self.add_widget(save_button)

        delete_button = MDFillRoundFlatIconButton(
            text="Delete",
            icon="delete",
            size_hint=(.9 / 3 - .05 / 2, None),
            pos_hint={
                'y': .03,
                'x': 0.075 + 2 * .9 / 3
            },
            on_press=self.delete_subject
        )
        delete_button.md_bg_color = delete_button.theme_cls.error_color
        self.add_widget(delete_button)

    def go_back(self, *args, **kwargs):
        go_back()
        with open(get_root() + f'/data/subjects/{self.name}.txt', encoding="UTF-8") as txtfile:
            text: str = txtfile.read()
        self.text_input.text = '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'+text

    def save_edit(self, *args, **kwargs):
        text: list[str] = self.text_input.text.split('\n')
        for _ in range(text.count('')):
            text.remove('')
        text: str = '\n'.join(text)

        with open(get_root() + f'/data/subjects/{self.name}.txt', 'w', encoding="UTF-8") as txtfile:
            txtfile.write(text)

        go_back()

    def delete_subject(self, *args, **kwargs):
        try:
            os.remove(get_root() + f'/data/subjects/{self.name}.txt')
            go_back()
        except FileNotFoundError:
            content = MDLabel(
                text="This is subject doesn't exist, or was removed!",
                halign='center',
                valign='middle',
            )
            content.font_size = 70
            content.bind(size=content.setter('text_size'))
            content.color = content.theme_cls.primary_color
            popup = Popup(
                title="DELETE SUBJECT ERROR",
                content=content
            )
            content.bind(on_touch_down=popup.dismiss)
            popup.open()

    def go_to_me(self, *args, **kwargs):
        SubjectsUpdater.current_sm(self.name)


class AddSubjectScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        label = MDLabel(
            text="Add Subject",
            halign='center',
            valign='top'
        )
        label.font_size = 70
        label.bind(size=label.setter('text_size'))
        label.color = label.theme_cls.primary_color
        self.add_widget(label)

        self.name_input = MDTextField(
            mode="rectangle",
            hint_text='Name',
            helper_text='Latin name by one word, or with_underscores-or-dash',
            required=True,
            size_hint=(.9, .1),
            pos_hint={
                'center_x': .5,
                'y': 1-.2-.1
            }
        )
        self.name_input.line_color_normal = self.name_input.theme_cls.primary_color
        self.name_input.hint_text_color_normal = self.name_input.theme_cls.primary_color
        self.name_input.line_color_focus = self.name_input.theme_cls.accent_color
        self.add_widget(self.name_input)

        self.text_input = MDTextField(
            mode="fill",
            text='\n\n\n\n\n\n\n\n\n\n',
            hint_text='Messages',
            helper_text='Every new line is another message',
            required=True,
            multiline=True,
            size_hint=(0.9, .5),
            max_height=Window.size[1]*(.5-.03),
            pos_hint={
                'center_x': .5,
                'y': .2
            }
        )
        self.text_input.line_color_normal = self.text_input.theme_cls.primary_color
        self.text_input.hint_text_color_normal = self.text_input.theme_cls.primary_color
        self.text_input.line_color_focus = self.text_input.theme_cls.accent_color
        self.add_widget(self.text_input)

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
            icon="book-plus",
            size_hint=(.9/2-.05/2, None),
            pos_hint={
                'y': .03,
                'x': 1-.05-.9/2+.05/2
            },
            on_press=self.add_subject
        )
        self.add_widget(add_button)

    def go_back(self, *args, **kwargs):
        go_back()
        self.name_input.text = ''
        self.text_input.text = '\n\n\n\n\n\n\n\n\n\n'

    def add_subject(self, *args, **kwargs):
        path = get_root() + f'/data/subjects/{self.name_input.text}.txt'

        content = MDLabel(
            text="Unknown ERROR!",
            halign='center',
            valign='middle',
        )
        content.font_size = 70
        content.bind(size=content.setter('text_size'))
        content.color = content.theme_cls.primary_color
        popup = Popup(
            title="ADD SUBJECT ERROR",
            content=content
        )
        content.bind(on_touch_down=popup.dismiss)

        if os.path.exists(path):
            content.text = "This subject already exists!"
            popup.open()
            return

        if self.name_input.text == '':
            content.text = "Should write a subject name!"
            popup.open()
            return

        text: list[str] = self.text_input.text.split('\n')
        for _ in range(text.count('')):
            text.remove('')
        text: str = '\n'.join(text)

        if text == '':
            content.text = "Should write a subject text!"
            popup.open()
            return

        with open(path, 'w', encoding="UTF-8") as txtfile:
            txtfile.write(text)

        self.go_back()


def go_back_setup(*args, **kwargs):
    from app.screens.setup import current
    current("main")


class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        label = MDLabel(
            text="Subjects Settings",
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
            size_hint=(.5, .6),
            pos_hint={'center_x': .5, 'y': .2}
        )

        self.bl = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=0
        )
        
        self.sv.add_widget(self.bl)
        self.add_widget(self.sv)

        add_subject_button = MDFillRoundFlatIconButton(
            text="Add subject",
            icon="book-plus",
            size_hint=(.9, None),
            pos_hint={
                'center_x': .5,
                'y': .03
            },
            on_press=self.go_to_add_subject
        )
        self.add_widget(add_subject_button)

    def update_canvas(self, *args, **kwargs):
        self.remove_widget(self.sv)

        self.sv = MDScrollView(
            do_scroll_x=False,
            size_hint=(.5, .6),
            pos_hint={'center_x': .5, 'y': .2}
        )

        self.bl = MDBoxLayout(
            id="bl",
            orientation="vertical",
            size_hint_y=None,
            height=0
        )

        self.sv.add_widget(self.bl)
        self.add_widget(self.sv)

        for screen in SubjectsUpdater.screens():
            label = MDRectangleFlatButton(
                id=screen.name,
                text=screen.name,
                size_hint=(1, None),
                on_press=screen.go_to_me
            )
            self.bl.add_widget(label)
            self.bl.height = self.bl.height + label.size[1]

    @staticmethod
    def go_to_add_subject(*args, **kwargs):
        SubjectsUpdater.current_sm("add_subject")


class SubjectsUpdater:
    _current_sm: str = "main"
    _need_update: bool = False
    _screens: list[SubjectScreenTemplate] = []

    @classmethod
    def current_sm(cls, current_sm: str = None) -> str:
        if current_sm:
            cls._current_sm = current_sm
        return cls._current_sm

    @classmethod
    def need_update(cls, need_update: bool = None) -> bool:
        if type(need_update) is bool:
            cls._need_update = need_update
        return cls._need_update

    @classmethod
    def screens(cls, screens: list[SubjectScreenTemplate] = None) -> list[SubjectScreenTemplate]:
        if screens:
            cls._screens = screens
        return cls._screens


class SubjectsScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.subjects_sm = MDScreenManager()

        self.main_screen = MainScreen(name="main")
        self.subjects_sm.add_widget(self.main_screen)
        self.add_subject = AddSubjectScreen(name="add_subject")
        self.subjects_sm.add_widget(self.add_subject)

        self.add_widget(self.subjects_sm)

        self.update_current_subjects_sm()
        self.update_main_and_screens()
        self.check_need_update()

    def update_current_subjects_sm(self, *args, **kwargs):
        self.subjects_sm.current = SubjectsUpdater.current_sm()
        Clock.schedule_once(self.update_current_subjects_sm)

    def update_main_and_screens(self):
        for screen in SubjectsUpdater.screens():
            self.subjects_sm.remove_widget(screen)
        screens: list[SubjectScreenTemplate] = []
        for subject in self.get_subjects().keys():
            screen = SubjectScreenTemplate(name=subject)
            screens.append(screen)
            self.subjects_sm.add_widget(screen)
        SubjectsUpdater.screens(screens)
        self.main_screen.update_canvas()

    def check_need_update(self, *args, **kwargs):
        if SubjectsUpdater.need_update():
            self.update_main_and_screens()
            SubjectsUpdater.need_update(False)
        Clock.schedule_once(self.check_need_update)

    @staticmethod
    def get_subjects() -> dict[str]:
        subjects = [subject[:-4] for subject in os.listdir(get_root() + '/data/subjects/')]
        subjects.remove('none')

        formatted_subjects: dict[str] = dict()
        for subject in subjects:
            with open(get_root() + f'/data/subjects/{subject}.txt', encoding="UTF-8") as txtfile:
                formatted_subjects[subject] = txtfile.read()

        return formatted_subjects
