from django.urls import path
from . import views
urlpatterns = [
    path('', views.BasePage.show_page, name='home'),
    path('<int:pk>/', views.CarDetailView.as_view())
]
