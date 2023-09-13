
What can this bot to do?
sends subjects messages to group by the schedule,
and write time for the next lesson. He has list of commands,
for another pupils its just get lesson schedules and time schedule,
and for admins to stop, resume, change subject for a day, and stop the bot for the appointed time.


Setup before starting:
1. Create new bot by https://t.me/BotFather, setup it anyhow u want.
2. Go to .env.dist and reformat it just to .env (without .dist)
3. In .env change BOT_TOKEN to your bot token, in GROUP_ID write id of your school group, and you can set admins by space key, also write ids of them
4. Go to data folder by path %ROOT%\data
5. Change subjects list >> just create file with name of subject in txt format file
6. In subjects_schedules change schedules.json where start from names of weeks, after weeakdays (from 0 to 6) and only then subjects
7. Than add also photo of schedule (if you have .pdf, then just convert it to .png) call it like schedules.png
8. In time_schedule change time schedule in schedule.json
9. Then also change time schedule text (schedule.txt)
10. Go to config.ini, but when u had already read config readme file, set parameters like you need.


To start the code:
1. run starter.cmd
2. write in that console "main.py"


Notation:
if you need to change some texts in command handlers,
then go to directory by %ROOT%\tgbot\handlers\handlers
and you can change every command!