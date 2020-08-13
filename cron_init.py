#!/usr/bin/env python3
from crontab import CronTab

cron = CronTab(user=True)
job = cron.new(command="$HOME/alariss-scheduler/bin/python $HOME/scheduler_app/send_reminders.py")
job.every().dom()

cron.write()