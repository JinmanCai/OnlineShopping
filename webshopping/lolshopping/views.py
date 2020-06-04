from django.shortcuts import render
from .models import Champions



def home(request):
    champ = Champions.objects.all()
    return render(request,'design/home.html',{'all':champ})
# Create your views here.
