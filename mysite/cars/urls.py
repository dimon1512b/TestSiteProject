from django.urls import path
from . import views
urlpatterns = [
    path('', views.base_page, name='home'),
    path('<int:id>/', views.detail_car),
    #path('filter', views.filters),
]
