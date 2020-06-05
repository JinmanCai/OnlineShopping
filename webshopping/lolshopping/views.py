from django.shortcuts import render
from .models import Champions



def home(request):
    champ = Champions.objects.all()
    return render(request,'design/home.html',{'all':champ})
# Create your views here.

def cart(request):
    context = {}
    return render(request, 'design/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'design/checkout.html', context)

