from Scrap_App import views
from django.urls import path
urlpatterns =[
    path("links/",views.LinksView.as_view(),name="links"),
    
]