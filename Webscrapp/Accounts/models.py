from django.db import models
from django.contrib.auth import get_user_model
from Webscrapp import choices
# Create your models here.

User = get_user_model()
class user_subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.CharField(null=True, max_length=255, blank=True,choices=choices.user_subscription_choices)

class job(models.Model):
    url = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    priority =models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True,choices=choices.job_status_choices,default='new')

class JobQueue(models.Model):
    job = models.ForeignKey(job,on_delete=models.CASCADE)
    queue = models.IntegerField()
