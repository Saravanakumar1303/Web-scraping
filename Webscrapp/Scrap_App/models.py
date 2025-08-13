from django.db import models
from django.contrib.auth import get_user_model
from Webscrapp import choices # type: ignoredoc
from Accounts.models import job

User = get_user_model()

class Links(models.Model):
    job =models.ForeignKey(job,on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    status_code = models.IntegerField()
    is_valid = models.BooleanField(default=False)
    status = models.BooleanField(default=False)

class SiteAuditModel(models.Model):
    links = models.ForeignKey(Links, on_delete=models.CASCADE)
    missing_h1 = models.BooleanField(default=False)
    mutiple_h1_count = models.IntegerField(default=0)
    mutiple_h1_tags = models.JSONField(default=list)
    missing_title = models.BooleanField(default=False)
    missing_desc = models.BooleanField(default=False)
    multiple_title_count = models.IntegerField(default=0)
    multiple_title_tags = models.JSONField(default=list)
    missing_alt = models.IntegerField(default=0)
    missing_alt_tags =models.JSONField(default=list)


