from django.urls import path  # This path function helps configure the path requested and the view utilized

from . import views  # importing the views.py from the same directory. Now all the designed views are available here


urlpatterns = [
    path('', views.home, name="homepage"),
    path('about', views.about, name="aboutpage"),
    path('addProduct', views.AddProduct.as_view(), name="addProduct"),
    path('products', views.ProductList.as_view(), name="products"), 
    path('products/<int:id>', views.product_details, name="p_details" ),
    path('editProd/<int:pk>', views.EditProduct.as_view(), name="editProd"),
    path('search', views.searchView, name='search')
]

