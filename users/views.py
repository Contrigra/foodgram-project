from django.contrib.auth import login
# Create your views here.
from users.forms import CreationForm
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseBadRequest

# TODO static for account/login

def sign_up_view(request):
    context = {}
    form = CreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/')

    context['form'] = form
    return render(request, 'registration/sign_up.html', context)


    # TODO
def password_change_view(request):
    pass

def password_reset_view(request):
    pass