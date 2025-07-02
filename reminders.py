import json
import os
import asyncio
from datetime import datetime, timedelta

REMINDERS_FILE = 'reminders.json'

class ReminderManager:
    def __init__(self):
        self.reminders = []
        self.load_reminders()
        self.scheduled_tasks = []

    def load_reminders(self):
        if os.path.exists(REMINDERS_FILE):
            with open(REMINDERS_FILE, 'r') as f:
                self.reminders = json.load(f)
        else:
            self.reminders = []

    def save_reminders(self):
        with open(REMINDERS_FILE, 'w') as f:
            json.dump(self.reminders, f, indent=2)

    def add_reminder(self, medication, time_str, frequency='daily'):
        reminder = {
            'medication': medication,
            'time': time_str,  # '08:00' format
            'frequency': frequency,
            'active': True,
            'last_reminded': None
        }
        self.reminders.append(reminder)
        self.save_reminders()
        return reminder

    def list_reminders(self):
        return [r for r in self.reminders if r['active']]

    def remove_reminder(self, medication, time_str=None):
        for r in self.reminders:
            if r['medication'] == medication and (time_str is None or r['time'] == time_str):
                r['active'] = False
        self.save_reminders()

    def update_reminder(self, medication, new_time=None, new_frequency=None):
        for r in self.reminders:
            if r['medication'] == medication and r['active']:
                if new_time:
                    r['time'] = new_time
                if new_frequency:
                    r['frequency'] = new_frequency
        self.save_reminders()

    def mark_as_taken(self, medication):
        now = datetime.now().isoformat()
        for r in self.reminders:
            if r['medication'] == medication and r['active']:
                r['last_reminded'] = now
        self.save_reminders()

    async def schedule_reminders(self, speak_func):
        while True:
            now = datetime.now()
            for r in self.reminders:
                if not r['active']:
                    continue
                reminder_time = datetime.strptime(r['time'], '%H:%M').replace(
                    year=now.year, month=now.month, day=now.day)
                if now >= reminder_time and (not r['last_reminded'] or now.date() != datetime.fromisoformat(r['last_reminded']).date()):
                    await speak_func(f"It's {r['time']}. Time to take your {r['medication']}.")
                    r['last_reminded'] = now.isoformat()
                    self.save_reminders()
            await asyncio.sleep(60)  # Check every minute

# Singleton instance
reminder_manager = ReminderManager() 