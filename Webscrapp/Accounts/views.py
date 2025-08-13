from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import get_user_model,authenticate,login,logout
import re
from Accounts.models import job,JobQueue,user_subscription
from django.views import View
from Webscrapp import choices
from django.contrib import messages

user = get_user_model()
# Create your views here.

class Dashboard(View):
    def get(self, request): # type: ignore
        return render(request,'dashboard.html',{'user':request.user}) 
    

class RegisterUser(View):

    def check_password(self,passwd):
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$" # type: ignore
        pat = re.compile(reg)
        mat = re.search(pat, passwd)
        if mat:
            return True
        else:
            return False
        
    def post(self,request):
        first_name = request.POST.get('fname')
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = None
        try:
            if email and password:
                valid_email = re.match(r'^[a-zA-Z0-9._%+-]+@gmail.com$', email)
                if not valid_email:
                    print("Invalid Email")
                    return redirect("register")
                if not self.check_password(password): # type: ignore
                    print("Invalid Password")
                    return redirect("register")

                user = get_user_model().objects.create(
                    first_name = first_name,
                    username = email,
                    email = email,
                )
                user.set_password(password)
                user.save()
        except Exception as e:
            print(e)
        return redirect('login')
    
    def get(self,request):
        return render(request,'register.html')

class LoginView(View):
    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                #print("Login Successfully.")
                messages.error(request, "Login Successfully")
                return redirect("dashboard")
            else:
                #print("Invalid Credentials")
                messages.error(request,"Invalid Credentials")
                return redirect("login")
        print("Invalid Usernmae and password")
        messages.error(request, "Invalid username and password!")
        return redirect('login')
    
    def get(self,request):
        return render(request,'login.html')
    
class Logout(View):
    def get(self,request):
        logout(request)
        return redirect("dashboard")

class create_job(View):
    def post(self, request):
        url = request.POST.get('url')
        print("url :",url)
        status = request.POST.get('status')
        print("status :",status)
        user = request.user
        print("user :",user)

        # Check if the user is authenticated
        if not user.is_authenticated:
            return redirect('login')  # Or wherever your login view is

        user_sub = user_subscription.objects.filter(user=user).first()
        

        if not user_sub:
            return redirect('job')  # User has no subscription, cannot create job

        # Determine priority based on subscription type
        if user_sub.subscription == choices.user_subscription_pro:  # type: ignore
            priority = 1
        elif user_sub.subscription == choices.user_subscription_basic:  # type: ignore
            priority = 2
        elif user_sub.subscription == choices.user_subscription_free:  # type: ignore
            priority = 3
        else:
            priority = 3  # Default fallback

        # Only create job if both URL and status are provided
        if url and status:
            job.objects.create(
                url=url,
                user=user,
                priority=priority,
                status=status
            )

        return redirect('job')

    def get(self, request):
        jobs = job.objects.all().values("id", "url", "user__username", "priority", "status")
        return render(request, 'jobs.html', {'jobs': jobs, 'choices': choices.job_status_choices})

class Subscription(View):
    def get(self,request):
        Sub = user_subscription.objects.all().values('id','user__first_name','subscription')
        return render(request,'subscription.html',{'subscription_table':Sub,'choices':choices.user_subscription_choices})
    
    def post(self,request):
        subscription_type = request.POST.get('subscription')
        if subscription_type:
            user_subscription.objects.create(
                user = request.user,
                subscription = subscription_type
            )
            return redirect('job')