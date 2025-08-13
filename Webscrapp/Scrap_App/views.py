from django.shortcuts  import render
from django.views import View
from Scrap_App.models import Links
from Accounts.models import job
from Webscrapp import choices


class LinksView(View):
    def get(self,request):
        jobs_obj =job.objects.filter(user=request.user,status=choices.job_status_completed).first()
        link = Links.objects.filter(job=jobs_obj,status_code=200).values()
        return render(request,'linkview.html',{'link':link})
    