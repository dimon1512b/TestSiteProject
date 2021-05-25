from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Cars


class BasePage:

	def show_page(self):
		data = Cars.objects.order_by('date_created')
		paginator = Paginator(data, 20)
		page_number = self.GET.get('page')
		page_obj = paginator.get_page(page_number)
		return render(self, 'cars/base.html', {'data': data, 'page_obj': page_obj})
