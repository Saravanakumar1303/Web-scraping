from django.urls import path,include
from Accounts import views

urlpatterns = [
    path("",views.Home.as_view(), name="home"),
    path("register/",views.RegisterUser.as_view(), name="register"),
    path("login/",views.LoginView.as_view(), name="login"),
    path("logout/",views.Logout.as_view(), name="logout"),
    path("jobs/create/",views.create_job.as_view(), name="create_job"),
    path("jobs/",views.View_jobs.as_view(), name="jobs"),
    path("subs/",views.Create_Subscription.as_view(), name="subs"),
    path("view_subs/",views.View_Subscription.as_view(), name="view_subs"),
]