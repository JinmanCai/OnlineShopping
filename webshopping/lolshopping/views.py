from django.shortcuts import render



def home(request):
    return render(request,'design/home.html')
# Create your views here.
