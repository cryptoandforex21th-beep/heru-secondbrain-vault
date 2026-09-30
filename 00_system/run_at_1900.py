import time
import datetime
import subprocess

now = datetime.datetime.now()
target_time = now.replace(hour=19, minute=0, second=0, microsecond=0)

delay = (target_time - now).total_seconds()

if delay > 0:
    print(f"Waiting {delay:.1f} seconds until 19:00:00...")
    time.sleep(delay)

print("Executing WhatsApp send at 19:00...")
subprocess.run(['python', r'd:\SecondBrain\00_system\whatsapp_cli.py', 'glo mbg', 'ini pesan otomatis heru2.0, selamat malam'])
