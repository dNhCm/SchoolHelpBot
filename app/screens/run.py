import asyncio
import json
from multiprocessing import Process
from typing import Optional

from aiogram import Dispatcher, Bot
from kivy.graphics import Color
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.button import MDRectangleFlatButton, MDFillRoundFlatIconButton
from kivymd.uix.screen import MDScreen

from misc.logger import logger
from algorythms.subjects_algorythm.subjects import main as algorythm_main
from misc.root import get_root
from tgbot.bot import start as tgbot_start, build as tgbot_build


class WorkingControlButton(MDRectangleFlatButton):
    week: str = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.working_state = "run"
        self.working_count = 0
        self.work_process: Optional[Process] = None

        self.pos_hint = {'x': .5-.15, 'y': .5-.15}
        self.size_hint = (.3, .3)
        self.text = "Run"
        self.font_size = 50
        self.text_color = Color(50/255, 183/255, 108/255).rgb
        self.line_color = Color(50/255, 183/255, 108/255).rgb

    @staticmethod
    def start_main(week: str):
        async def tgbot(dp: Dispatcher, bot: Bot):
            try:
                await tgbot_start(dp, bot)
            except (KeyboardInterrupt, SystemExit):
                logger.error('Bot was stopped!')

        async def algorythm():
            print(week)
            await algorythm_main(week)

        async def main():
            dp, bot = tgbot_build()

            await asyncio.gather(
                tgbot(dp, bot),
                algorythm(),
            )

        asyncio.run(main())

    def on_touch_up(self, touch):
        if (
            self.pos[0] <= touch.x <= self.pos[0] + self.size[0]
            and self.pos[1] <= touch.y <= self.pos[1] + self.size[1]
        ):
            if self.working_state == "run":
                self.text = "Stop"
                self.text_color = Color(170/255, 13/255, 24/255).rgb
                self.line_color = Color(170/255, 13/255, 24/255).rgb
                self.work_process = Process(
                    name="tgbot",
                    target=self.start_main,
                    args=(self.week,)
                )
            elif self.working_state == "stop":
                self.text = "Run"
                self.text_color = Color(50/255, 183/255, 108/255).rgb
                self.line_color = Color(50/255, 183/255, 108/255).rgb
            else:
                logger.warning(f"!!! state of WorkingControlButton was {self.working_state} so incorrect !!!")
                self.working_state = "run"

            self.working_count += 1
            if self.working_count == 2:
                if self.working_state == "run":
                    self.work_process.start()
                elif self.working_state == "stop":
                    self.work_process.terminate()

                self.working_state = "run" if self.working_state == "stop" else "stop"
                self.working_count = 0


class RunScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open(get_root()+'/data/subjects_schedules/schedules.json', encoding="UTF-8") as jsonfile:
            subjects_schedules: dict = json.load(jsonfile)

        def lbs_callback(schedule: str):
            WorkingControlButton.week = schedule
            current_week_btn.text = f"Current week: {schedule}"

        def open_lbs(*args):
            lbs = MDListBottomSheet()
            for schedule in subjects_schedules.keys():
                lbs.add_item(
                    text=schedule,
                    callback=lambda x, y=schedule: lbs_callback(y)
                )
            lbs.open()

        current_week_btn = MDFillRoundFlatIconButton(
            text=f"Current week: None",
            icon="",
            size_hint=(.9, None),
            pos_hint={
                'center_x': .5,
                'y': .05
            },
            on_press=open_lbs
        )

        self.add_widget(current_week_btn)
        self.add_widget(WorkingControlButton())
