from django.shortcuts import render
from .models import Champions
from .filters import ChampionsFilter



def home(request):
    champ = Champions.objects.all().order_by('name')

    myFilter = ChampionsFilter(request.GET, queryset=champ)

    champ = myFilter.qs

    context = {'all':champ, 'myFilter':myFilter}
    return render(request,'design/home.html',context)
# Create your views here.

def cart(request):
    context = {}
    return render(request, 'design/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'design/checkout.html', context)

