from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from users.forms import CreationForm
from django.contrib.auth import logout as auth_logout


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


