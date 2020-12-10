from django.http import HttpResponse
from django.shortcuts import render

#TODO сделать @login_required и там захардкодить ссылки на
# страницы для залогинненного и не залогиненного юзера.

def index_view(request):
    return render(request, 'indexNotAuth.html')