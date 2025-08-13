from Scrap_App.utils import ScrapPage
import asyncio
from Accounts.models import job


def run(*args):
    if not args:
        print("No job id passed")
        return
    
    job_id = int(args[0])
    print("job id :",job_id)

    jobs = job.objects.get(id=job_id)
    print("jobs: ",jobs)

    page =ScrapPage(jobs)
    asyncio.run(page.run_scrap())