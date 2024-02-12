from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils.decorators import method_decorator
from mysite.decorators import login_required
from django.db.models import Q
from .mail import email_verification_mail
from .models import User, ConfirmEmail


class Login(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_verified:
            messages.info(request, "You are already logged in, Logout first")
            return redirect("index")
        return render(request, "account/login.html")

    def post(self, request):
        uname = request.POST.get("username", "")
        passwd = request.POST.get("password", "")
        user = authenticate(username=uname, password=passwd)

        if user is not None:
            login(request, user)
            if not user.is_verified:
                return redirect("account:send_verification_otp")
            messages.success(request, "Logged in")
            return redirect("index")
        else:
            messages.warning(request, "Username or password is incorrect")
        return render(request, "account/login.html")

@method_decorator(login_required, name="dispatch")
class Logout(View):
    def get(self, request):
        logout(request)
        messages.info(request, "Logged out")
        return redirect("account:login")

class Register(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_verified:
            messages.info(request, "You are already logged in")
            return redirect("index")
        return render(request, "account/register.html")
    
    def post(self, request):
        data = request.POST
        passwd1 = data.get("password1", "")
        passwd2 = data.get("password2","")
        if passwd1 and (passwd1 != passwd2):
            messages.warning(request, "Passwords do not match")
            return redirect("account:register")
        
        email, username = data.get("email").lower(), data.get("username")
        if not (email and username):
            messages.info(request, "Email and username are required")
            return redirect("account:register")
        
        user = User.objects.filter(Q(email=email) | Q(username=username))
        if not user.exists():
            user = User(email=email, username=username)
            user.set_password(passwd1)
            user.save()
            login(request, user)
            return redirect("account:send_verification_otp")

        messages.info(request, "User already exists")
        return redirect("account:register")

class VerifyEmail(View):
    def get(self, request):
        if request.user.is_authenticated and not request.user.is_verified:
            return render(request, "account/verify_email.html")
        messages.info(request, "Either you are not logged in or already veried your account")
        return redirect("account:login")

    def post(self, request):
        if (otp := request.POST.get("otp")) and otp.isdigit() and len(otp) == 6:
            if cnfm := ConfirmEmail.objects.filter(user=request.user).first():
                cnfm.attempts = cnfm.attempts + 1
                cnfm.save()
                if cnfm.attempts > 5:
                    messages.warning(request, "You are already complete maximum attempts. Create new OTP")
                    cnfm.delete()
                    return redirect("account:send_verification_otp")
                if int(otp) == cnfm.otp:
                    if cnfm.is_expired():
                        cnfm.delete()
                        messages.info(request, "OTP is expired. We have just send you a new OTP")
                        return redirect("account:send_verification_otp")
                    request.user.is_verified = True
                    request.user.save()
                    messages.success(request, "Successfully verified email")
                    return redirect("index")
        messages.warning(request, "OTP is incorrect")
        return redirect("account:verify_email")

class SendVerificationOtp(View):
    def get(self, request):
        if request.user.is_authenticated and not request.user.is_verified:
            email_verification_mail(request.user)
            messages.info(request, "OTP is send to your email. Check spam golder if it didn't appears")
            return redirect("account:verify_email")
        else:
            messages.warning(request, "Your account is already verified")
            return redirect("index")
