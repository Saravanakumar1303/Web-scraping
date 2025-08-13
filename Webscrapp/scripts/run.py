from Scrap_App.utils import ScrapPage
from Accounts.models import job
import asyncio
from Webscrapp import choices
import time
import subprocess


def run():
    print("Script Started")
    while True:
        jobs = job.objects.filter(status=choices.job_status_new).order_by("priority") 
        print("jobs: ",jobs)
        if not jobs:
            print("No new jobs found")
            time.sleep(60)
            continue
        job_obj = jobs.first()
        print("job_obj",job_obj)
        if job_obj:
            subprocess.Popen(
                [
                    "python", "manage.py", "runscript", "scrap",
                    "--script-args", str(job_obj.id)
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                start_new_session=True
            )
            print("subprocess launched")
       
        time.sleep(10)
