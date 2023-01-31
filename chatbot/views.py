from email.mime import message
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from .main import chat

texts = []
# Create your views here.
def home(request):
    
    return render(request, 'index.html', {"bot" :texts, "range":range(0, len(texts))})


def handle(request):
    if request.method == 'POST':
        print(request.POST.get("msg"))
    texts.append(str(request.POST.get("msg")))
    texts.append(chat(str(request.POST.get("msg"))))
    return render(request, 'index.html', {"bot" :texts, "range":range(0, len(texts))})
