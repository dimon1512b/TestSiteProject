from django.urls import path
from . import views
urlpatterns = [
    path('', views.BasePage.show_page, name='home')
]
