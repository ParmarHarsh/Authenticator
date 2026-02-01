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
    """
    Renders the home page of the application.
    Displays the main interface with login/register options for unauthenticated users
    or a welcome message for authenticated users.
    """
    return render(request, "Authenticator/index.html")


def register_user(request):
    """
    Handles user registration process.
    Validates input data, creates inactive user account, sends welcome and activation emails.
    Redirects to login page on successful registration.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check if username already exists
        if User.objects.filter(username=username):
            messages.error(request, "Username Already Exists! Please Try Again.")
            return redirect("home")

        # Validate username length
        if len(username) > 10:
            messages.error(request, "Username Must Be Under 10 Characters! Please Try Again.")
            return redirect("home")

        # Validate username is alphanumeric
        if not username.isalnum():
            messages.error(request, "Username Must Be Alpha-Numeric! Please Try Again.")
            return redirect("home")

        # Check if email already registered
        if User.objects.filter(email=email):
            messages.error(request, "Email Already Registered! Please Try Again.")
            return redirect("home")

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords Did Not Match! Please Try Again.")
            return redirect("home")

        # Create user account (inactive by default)
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = False
        user.save()

        messages.success(request, "Your Account Has Been Created! Please Check Your Email To Activate Your Account.")

        # Send welcome email
        subject = "Welcome to Desk AI!"
        message = "Hello " + user.first_name + "! \n \n" + "Thank you for visiting our website and welcome to Desk AI. \n \n" + "In order to activate your account, please lookout for an email with the following subject line 'Account Activation - Desk AI' sent to your email address. \n \n" + "Sincerely, \n" + "Harsh Parmar"
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Send account activation email
        current_site = get_current_site(request)
        subject_confirmation = "Account Activation - Desk AI"
        message_confirmation = render_to_string("confirmation_email.html", {
            'name': user.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user),
        })

        email = EmailMessage(
            subject_confirmation,
            message_confirmation,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email.fail_silently = True
        email.send()

        return redirect("login_user")

    return render(request, "Authenticator/register_user.html")


def login_user(request):
    """
    Handles user login process.
    Authenticates user credentials and logs them in if valid.
    Redirects to home page on successful login.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            first_name = user.first_name
            return render(request, "Authenticator/index.html", {'first_name': first_name})
        else:
            messages.error(request, "Incorrect Username/Password! Please Try Again.")
            return redirect("home")

    return render(request, "Authenticator/login_user.html")


def logout_user(request):
    """
    Handles user logout process.
    Logs out the current user and redirects to home page with success message.
    """
    logout(request)
    messages.success(request, "You Have Successfully Logged-Out!")
    return redirect("home")


def activate(request, uidb64, token):
    """
    Handles account activation via email link.
    Decodes user ID from URL, verifies token, and activates account if valid.
    Logs in the user automatically after activation.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        first_name = user.first_name
        return render(request, "Authenticator/index.html", {'first_name': first_name})
    else:
        return render(request, "activation_fail.html")