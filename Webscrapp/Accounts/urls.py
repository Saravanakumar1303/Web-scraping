from django.urls import path,include
from Accounts import views

urlpatterns = [
    path("",views.Dashboard.as_view(), name="dashboard"),
    path("register/",views.RegisterUser.as_view(), name="register"),
    path("login/",views.LoginView.as_view(), name="login"),
    path("logout/",views.Logout.as_view(), name="logout"),
    path("jobs/",views.create_job.as_view(), name="job"),
    path("subs/",views.Subscription.as_view(),name="subs"),
]