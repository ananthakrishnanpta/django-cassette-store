from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.template import loader # this module helps load html template
from django.views.generic import ListView, CreateView
from .models import Product
# from .forms import AddProductForm
# Create your views here.


# def home(request):
#     return HttpResponse("Hi, This is my home page !")

def home(request):
    products = Product.objects.all() # collecting all the products
    context = {
        'prods' : products,
        
    }
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context, request))

class ProductList(ListView):
    model  = Product
    template_name = 'products.html'


def about(request):
    # return HttpResponse("Hi, this is my about page !!!")
    template = loader.get_template('about.html')
    return HttpResponse(template.render())

class AddProduct(CreateView):
    model = Product
    template_name = "addProduct.html"
    fields = [
            'name',
            'price',
            'description',
            'stock',
            'pic'        
            ]

    success_url = "/"