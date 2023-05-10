
import asyncio
import json
import arrow
from aiogram import Dispatcher

from bot import logger
from tgbot.misc.now_in_schedules import we_in_time
from tgbot.misc.time_to_wait import wait


class WorkOn:
    week: str
    next_time: str
    subject: str|list
    next_subject: str|list
    next_message_id: int|None = None

    def __init__(self, dp: Dispatcher):
        self.dp = dp

    def preparing(self):  # Preparing for the looping the main piece of script (getting req)
        logger.info('Started preparing')
        while True:
            answer = input('Which week is now? (A, B): ')
            if not answer in ['A', 'B']: continue
            else: break
        self.week = answer

        schedules = json.load(open('data/schedules/schedules.json'))
        try:
            self.next_time = we_in_time(schedules)
        except:
            logger.warning('Today wont be lessons more!')
            schedules = json.load(open('data/schedules/schedules.json'))
            self.next_time = schedules[0][0]
        logger.info('Finished preparing successfully!')

    def subjects(self, schedules: list[list[str]], subjects_schedule: dict[list[str]], consultations: dict[list[str]]):  # Getting by algorythm the subject what will be
        now = arrow.now()
        for ischedule, schedule in enumerate(schedules):
            for itime, time in enumerate(schedule):
                if time == self.next_time:
                    try:
                        if ischedule in [0, 1]:
                            self.subject = subjects_schedule[self.week][now.weekday()][itime]
                            try:
                                self.next_subject = subjects_schedule[self.week][now.weekday()][itime + 1]
                            except:
                                self.next_subject = subjects_schedule[self.week][now.weekday() + 1][itime]
                        elif ischedule in [2]:
                            self.subject = consultations['1'][now.weekday()][itime]
                            try:
                                self.next_subject = consultations['1'][now.weekday()][itime + 1]
                            except:
                                self.next_subject = consultations['1'][now.weekday() + 1][0]
                    except:
                        logger.warning('Today is a weekend!')
                        self.subject = 'none'
                        self.next_subject = 'none'

    async def waiting(self):  # Waiting for the time, when will send the code and link to lesson
        bot = self.dp.bot
        time_to_wait = wait(self.next_time)
        for time in range(time_to_wait // 60):
            logger.info(f'Waiting {(time_to_wait - 60 * time) / 60} mins')
            if not self.next_message_id is None:
                await bot.edit_message_text(
                    message_id=self.next_message_id,
                    chat_id=bot['config'].tgbot.group_id,
                    text=f'Наступний урок: {self.next_subject_str}\nЗалишилося часу до наступного уроку: {((time_to_wait - 60 * time) // 60) + 5} хвилин (+- 1 хвилина)'
                )
            await asyncio.sleep(60)
        logger.info(f'Waiting {time_to_wait - time_to_wait // 60 * 60} secs')
        await asyncio.sleep(time_to_wait - time_to_wait // 60 * 60)
        if not self.next_message_id is None:
            await bot.delete_message(message_id=self.next_message_id, chat_id=bot['config'].tgbot.group_id)

    def update_next_time(self, schedules):  # Set the time of the next lesson to next one
        for ischedule, schedule in enumerate(schedules):
            for itime, time in enumerate(schedule):
                if time == self.next_time:
                    try:
                        self.next_time = schedule[itime + 1]
                    except:
                        try:
                            self.next_time = schedules[ischedule + 1][0]
                        except:
                            logger.warning('Its the end of a day!')
                            self.next_time = schedules[0][0]
                    break

    async def text(self):
        # Getting the text from data, and if the subject is list, then getting more texts
        logger.info('Getting text of the subject or subjects')
        if type(self.subject) is list:
            text = ''
            for subject in self.subject:
                with open(f'data/subjects/{subject}.txt', encoding='UTF-8') as f:
                    text += '\n' + ''.join(f.readlines())
        else:
            with open(f'data/subjects/{self.subject}.txt', encoding='UTF-8') as f:
                text = ''.join(f.readlines())
        logger.info(f'The text for sending:\n{text}')

        text_list = text.split('\n')

        # Sending text
        logger.info('Send the subject text')
        for text in text_list:
            try:
                bot = self.dp.bot
                await bot.send_message(chat_id=bot['config'].tgbot.group_id, text=text)
            except:
                pass
        logger.info('Sent successfully!')

    async def next_text(self):
        # Preparing next text
        logger.info('Preparing the next text')
        if not type(self.next_subject) is list:
            try:
                with open(f'data/subjects/{self.next_subject}.txt', encoding='UTF-8') as f:
                    self.next_subject_str = f.readlines()[-1]
            except:
                self.next_subject_str = ''
        else:
            for next_subject in self.next_subject:
                self.next_subject_str = ''
                try:
                    with open(f'data/subjects/{next_subject}.txt', encoding='UTF-8') as f:
                        self.next_subject_str += f.readlines()[-1] + '\t'
                except: continue
        if not self.next_subject_str == '':
            text = f'Наступний урок: {self.next_subject_str}\nЗалишилось часу до наступного уроку: {wait(self.next_time) // 60} хвилин (+- 1 хвилина)'
        else:
            text = ''

        logger.info(f'Will send:\n{text}')

        # Send next text
        try:
            bot = self.dp.bot
            msg = await bot.send_message(chat_id=bot['config'].tgbot.group_id, text=text)
            self.next_message_id = msg['message_id']
        except:
            self.next_message_id = None

    async def work_on(self):  # The loop side of the script, sending the links to lessons
        # Preparing before of working
        logger.info('Getting all data')
        schedules = json.load(open('data/schedules/schedules.json'))
        subjects_schedule = json.load(open('data/schedule/schedule.json'))
        consultations = json.load(open('data/consultations/consultations.json'))
        logger.info('Got all data successfully!')

        logger.info('Determining of subject')
        self.subjects(schedules, subjects_schedule, consultations)
        logger.info(f'WorkOn(...).subject: {self.subject}')

        logger.info('Start waiting ...')
        await self.waiting()
        logger.info('Waiting was gone!')

        logger.info('Preparing the next time for a next loop')
        self.update_next_time(schedules)
        logger.info(f'New WorkOn(...).next_time: {self.next_time}')

        logger.info('Start preparing and send messages')
        await self.text()
        await self.next_text()
        logger.info('Sent successfully!')


    # Main
    async def main(self):
        self.preparing()
        while True:
            logger.info('Loop!')
            await self.work_on()