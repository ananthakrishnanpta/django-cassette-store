from django.urls import path  # This path function helps configure the path requested and the view utilized

from . import views  # importing the views.py from the same directory. Now all the designed views are available here


urlpatterns = [
    path('', views.home, name="homepage"),
    path('about', views.about, name="aboutpage")
]

