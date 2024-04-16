from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm
from .authenticator import EmailBackend
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from .tokengenerator import account_activation_token
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.utils.encoding import force_bytes, force_str
from .models import Users
from django.core.exceptions import ObjectDoesNotExist

def signup(request):
    print('asdad',get_current_site(request))
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            auth = authenticate(username = form.cleaned_data['email'], password = form.cleaned_data['password1'])
            if auth is not None:
                site = get_current_site(request)
                message = render_to_string("authentication/verificationmail.html", {
                    'user': auth,
                    'domain': site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(auth.pk)),
                    'token': account_activation_token.make_token(auth)
                })
                print(urlsafe_base64_encode(force_bytes(auth.pk)),account_activation_token.make_token(auth))
                email = EmailMessage('Verification', message, to=[request.POST['email']])
                email.send()

                login(request, auth)
                return redirect("/core")
            else:
                print("Error occured")
        else:
            return render(request, "authentication/signup.html", context={'error': form.errors.as_json()})
    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        auth = authenticate(username = email, password = password)
        if auth is not None:
            login(request, auth)
            return redirect("/core")
        else:
            print("Error occured")
            return render(request, "authentication/signin.html", context={'error': 'Please enter the correct credentials for your account'})
    return render(request, "authentication/signin.html")

def activation(request, uidb64, token):
    try:
        uid =  force_str(urlsafe_base64_decode(uidb64))
        user = Users.objects.get(id=uid)
    except ObjectDoesNotExist:
        return print("error")
    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.save()
        return redirect('/verificationsuccess')
    else:
        return HttpResponse("Error while verification")


def verificationsuccess(request):
    return render(request, "authentication/verificationsuccess.html")