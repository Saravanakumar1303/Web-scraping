from django.contrib import admin
from Accounts.models import user_subscription,job,JobQueue
# Register your models here.

@admin.register(user_subscription)
class user_subscription_admin(admin.ModelAdmin):
    list_display =('user','subscription')
    list_filter =('subscription',)

@admin.register(job)
class job_admin(admin.ModelAdmin):
    list_display=('url','user','priority','status')
    list_filter =('priority',)

@admin.register(JobQueue)
class JobQueue_admin(admin.ModelAdmin):
    list_display=('job',"queue")