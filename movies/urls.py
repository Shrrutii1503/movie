from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/dashboard',views.home),
    path('movies/dashboard/',views.get_all),
    path('movies/dashboard/delete-item/<int:id>', views.delete_item),
    path('movies/dashboard/rent/rent-movie/<int:id>/<int:movie_id>', views.rent),
    path('movies/dashboard/rent/rent-movie/<int:id>',views.rent_movie),
    path('movies/add-movie',views.add_movie),
   
]