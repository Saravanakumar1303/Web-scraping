from django.contrib import admin
from Scrap_App.models import Links,SiteAuditModel
# Register your models here

@admin.register(Links)
class LinkAdmin(admin.ModelAdmin):
    list_display =("url","status_code","status")
    list_filter = ("is_valid","job","status_code","status")

@admin.register(SiteAuditModel)
class SiteAuditModel(admin.ModelAdmin):
    list_display =("links","missing_h1","mutiple_h1_count","mutiple_h1_tags","missing_title","missing_desc","multiple_title_count","multiple_title_tags","missing_alt","missing_alt_tags")
    list_filter = ("links",)