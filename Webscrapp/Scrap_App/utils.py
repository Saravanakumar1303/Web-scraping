from Scrap_App.models import Links,SiteAuditModel
from Accounts.models import job
from bs4 import BeautifulSoup
from Webscrapp import choices
from asgiref.sync import sync_to_async
from playwright.async_api import async_playwright

async def scrape_page_with_playwright(url: str):
    """
    Scrapes the given URL using Playwright and returns the response status and HTML content.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        response = await page.goto(url)

        status_code = int(response.status)
        html_content = await page.content()
        await browser.close()

        return status_code, html_content

class ScrapPage:

    def __init__(self, job: job):
        self.job = job
        self.url = job.url
        self.main_url = job.url

    async def run_scrap(self):
        self.job.status =choices.job_status_inprogress
        await sync_to_async(self.job.save)()
        while True:
            link_objs = await sync_to_async(list)(Links.objects.filter(job=self.job, status=False))
            if link_objs:
                link_obj = link_objs[0]
                self.url = link_obj.url

            try:
                status_code, html_content = await scrape_page_with_playwright(self.url)

                if status_code == 200:
                    links_objs = await sync_to_async(list)(Links.objects.filter(job=self.job, url=self.url))
                    if not links_objs:
                        link_obj = await sync_to_async(Links.objects.create)(
                            job=self.job,
                            url=self.url,
                            is_valid=True,
                            status=True,
                            status_code=status_code
                        )
                    else:
                        link_obj = links_objs[0]
                        link_obj.status = True
                        link_obj.is_valid = True
                        link_obj.status_code = status_code
                        await sync_to_async(link_obj.save)()

                await self.extract_links(html_content, link_obj)

            except Exception as e:
                print(f"Error while scraping webpage - {e}")
                return

            links_count = await sync_to_async(Links.objects.filter(job=self.job,status=True).count)()
            if links_count >= choices.links_limit:
                break
        self.job.status = choices.job_status_completed
        await sync_to_async(self.job.save)() 

    async def extract_links(self, html_content, link_obj):
        soup = BeautifulSoup(html_content, "html.parser")
        a_tags = soup.find_all("a")

        for a_tag in a_tags:
            href = a_tag.get("href")
            if href and str(href).startswith(self.main_url):
                exists = await sync_to_async(Links.objects.filter(job=self.job, url=href).exists)()
                if not exists:
                    await sync_to_async(Links.objects.create)(
                        job=self.job,
                        url=href,
                        is_valid=False,
                        status=False,
                        status_code=0
                    )

        h1_tags = soup.find_all("h1")
        title_tags = soup.find_all("title")
        meta_tags = soup.find_all("meta")
        img_tags = soup.find_all("img")

        site_audit_obj = SiteAuditModel()
        site_audit_obj.links = link_obj
        site_audit_obj.missing_h1 = len(h1_tags) == 0
        site_audit_obj.mutiple_h1_count = len(h1_tags)
        site_audit_obj.mutiple_h1_tags = [str(tag) for tag in h1_tags]

        site_audit_obj.missing_title = len(title_tags) == 0
        site_audit_obj.multiple_title_count = len(title_tags)
        site_audit_obj.multiple_title_tags = [str(tag) for tag in title_tags]

        site_audit_obj.missing_desc = not any(meta.get("name") == "description" for meta in meta_tags)

        missing_alt_tags = [str(img) for img in img_tags if not img.get("alt")]
        site_audit_obj.missing_alt = len(missing_alt_tags)
        site_audit_obj.missing_alt_tags = missing_alt_tags

        await sync_to_async(site_audit_obj.save)()