from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from LoginSystem import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from django.core.mail import EmailMessage

def home(request):
    return render(request, "Authenticator/index.html")

def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")
        
        if User.objects.filter(username=username):
            messages.error(request, "Username Already Exists! Please Try Again.")
            return redirect("home")
        
        if len(username) > 10:
            messages.error(request, "Username Must Be Under 10 Characters! Please Try Again.")
            return redirect("home")
        
        if not username.isalnum():
            messages.error(request, "Username Must Be Alpha-Numeric! Please Try Again.")
            return redirect("home")
        
        if User.objects.filter(email=email):
            messages.error(request, "Email Already Registered! Please Try Again.")
            return redirect("home")
        
        if pass1 != pass2:
            messages.error(request, "Passwords Did Not Match! Please Try Again.")
            return redirect("home")
        
        user_detail = User.objects.create_user(username, email, pass1)
        user_detail.first_name = fname
        user_detail.last_name = lname

        user_detail.is_active = False

        user_detail.save()

        messages.success(request, "Your Account Has Been Created! Please Check Your Email To Activate Your Account.")

        # Welcome Email
        subject = "Welcome to Desk AI!"

        message = "Hello " + user_detail.first_name + "! \n \n" + "Thank you for visiting our website and welcome to Desk AI. \n \n" + "In order to activate your account, please lookout for an email with the following subject line 'Account Activation - Desk AI' sent to your email address. \n \n" + "Sincerely, \n" + "Harsh Parmar"

        from_email = settings.EMAIL_HOST_USER
        to_list = [user_detail.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Confirmation Email
        current_site = get_current_site(request)
        subject_con = "Account Activation - Desk AI"

        message_con = render_to_string("confirmation_email.html", {
                                            'name': user_detail.first_name,
                                            'domain': current_site.domain,
                                            'uid': urlsafe_base64_encode(force_bytes(user_detail.pk)),
                                            'token': generate_token.make_token(user_detail),
                                        })
        
        email = EmailMessage(
                    subject_con, 
                    message_con, 
                    settings.EMAIL_HOST_USER, 
                    [user_detail.email],
                )
        
        email.fail_silently = True
        email.send()

        return redirect("login_user")

    return render(request, "Authenticator/register_user.html")

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        pass1 = request.POST.get("pass1")

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name

            return render(request, "Authenticator/index.html", {'fname': fname})
        
        else:
            messages.error(request, "Incorrect Username/Password! Please Try Again.")

            return redirect("home")

    return render(request, "Authenticator/login_user.html")

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Successfully Logged-Out!")

    return redirect("home")

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user_detail = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user_detail = None

    if user_detail is not None and generate_token.check_token(user_detail, token):
        user_detail.is_active = True
        user_detail.save()

        login(request, user_detail)
        fname = user_detail.first_name

        return render(request, "Authenticator/index.html", {'fname': fname})
    else:
        return render(request, "activation_fail.html")