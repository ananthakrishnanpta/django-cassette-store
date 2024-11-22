from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.template import loader # this module helps load html template
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
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

def product_details(request, id):
    product = Product.objects.get(id = id)
    context = {
        'product' : product
    }
    template = loader.get_template('prod_details.html')
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


class EditProduct(UpdateView):
    model = Product
    template_name = "EditProduct.html"
    fields = [
            'name',
            'price',
            'description',
            'stock',
            'pic'        
            ]
    success_url = "/"



def searchView(request):
    query = request.GET.get('q1')
    results = Product.objects.filter(name__icontains=query) # filtering the product objects according string matching query
    # In the SQL => select * from Products where name like '%query%';
    context = {
        'prods' : results,
        'query' : query,
        'owner' :"surya",
        "items" : len(results)
    }
    
    template = loader.get_template('search_results.html')
    return HttpResponse(template.render(context, request))

class ProductSearchView(ListView):
    model = Product
    template_name = 'search_results.html'
    context_object_name = 'prods'

    # by default, this method of ListView collects all objects of the given class name
    # we are overriding and altering the method to collect only the objects with name containing the search string
    def get_queryset(self):
        query = self.request.GET.get('q1')
        if query:
            return Product.objects.filter(name__icontains=query)
        # This will 
        return Product.objects.all()
    
    # overrides the method which provides the context data, 
    # adds more key-value pairs to the dict and returns it
    # this will alter the context data before sending for rendering with template

    def get_context_data(self, **kwargs):
        default_context =  super().get_context_data(**kwargs) 
        # getting the default context variables using superclass method
        query = self.request.GET.get('q1','')
        default_context['query'] = query
        return default_context
