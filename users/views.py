from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render

from users.forms import CreationForm


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
