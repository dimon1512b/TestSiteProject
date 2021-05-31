from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import render
from .models import Cars
from django.db.models import Q


data_brand = {obj.brand for obj in Cars.objects.all()}
data_model = {obj.model for obj in Cars.objects.all()}
data_transmission = {obj.transmission for obj in Cars.objects.all()}
data_region = sorted({obj.region for obj in Cars.objects.all()})
data_city = sorted({obj.city for obj in Cars.objects.all()})
data_engine_type = {obj.engine_type for obj in Cars.objects.all()}
data_body_type = {obj.body_type for obj in Cars.objects.all()}
data_drive_type = {obj.drive_type for obj in Cars.objects.all()}
data_year = sorted({obj.year for obj in Cars.objects.all()})
data_engine_capacity = {obj.engine_capacity for obj in Cars.objects.all()}

data_filter = {'brand': data_brand, 'model': data_model, 'transmission': data_transmission, 'region': data_region,
               'city': data_city, 'engine_type': data_engine_type, 'body_type': data_body_type,
               'drive_type': data_drive_type, 'year': data_year, 'engine_capacity': data_engine_capacity}


def filters(request):
	print('filter def')
	full_path = HttpRequest.get_full_path(request)
	request_get = request.GET
	filter = Cars.objects.all()
	for param in request_get:
		if param == 'price_from' and request_get.get(param) != '':
			print('Условие price_from СРАБОТАЛО!')
			filter = filter.filter(price_usd__gte=str(request_get.get(param)))
			continue
		elif param == 'price_to' and request_get.get(param) != '':
			filter = filter.filter(price_usd__lte=request_get.get(param))
			continue
		elif param == 'body_type':
			filter = filter.filter(body_type=request_get.get(param))
			continue
		elif param == 'brand':
			filter = filter.filter(brand=request_get.get(param))
			continue
		elif param == 'model':
			filter = filter.filter(model=request_get.get(param))
			continue
		elif param == 'year':
			filter = filter.filter(year=request_get.get(param))
			continue
		elif param == 'region':
			filter = filter.filter(region=request_get.get(param))
			continue
		elif param == 'city':
			filter = filter.filter(city=request_get.get(param))
			continue
		elif param == 'engine_capacity':
			filter = filter.filter(engine_capacity=request_get.get(param))
			continue
		elif param == 'engine_type':
			filter = filter.filter(engine_type=request_get.get(param))
			continue
		elif param == 'transmission':
			filter = filter.filter(transmission=request_get.get(param))
			continue
		elif param == 'drive_type':
			filter = filter.filter(drive_type=request_get.get(param))
			continue
		print(param)
		print(type(param))
	print(filter)
	paginator_f = Paginator(filter, 5)
	page_number = request.GET.get('page')
	page_obj_1 = paginator_f.get_page(page_number)

	return render(request, 'cars/base.html', {'data': page_obj_1.object_list,
	                                          'data_filter': data_filter,
	                                          'page_obj': page_obj_1,
	                                          'request': request,
	                                          'full_path': full_path})


def base_page(request):
	print('base_page def')
	print(f'REQUEST IS {request}')
	print(f'REQUEST IS {request.GET}')
	full_path = HttpRequest.get_full_path(request)
	print(f'full_path {full_path}')
	data = Cars.objects.order_by('date_created')
	paginator = Paginator(data, 5)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number) # Ссылка на конкретную страницу пагинатора
	for i in data_filter:
		if request.GET.get(i):
			print('filter def get(i)')
			return filters(request)
	if (request.GET.get('price_from') not in ('', None)) or  (request.GET.get('price_to') not in ('', None)):
		print('filter def price')
		print(request.GET.get('price_from'))
		print(request.GET.get('price_to '))
		return filters(request)
	else:
		return render(request, 'cars/base.html', {
			'data': page_obj.object_list,
			'page_obj': page_obj,
			'data_filter': data_filter,
			'request': request,
			'full_path': full_path})


def detail_car(request, id):
	print('detail_car def')
	car = Cars.objects.get(pk=id)
	print(f'it is request: ===>>> {request}')
	print(f'it is type request: ===>>> {type(request)}')
	print(f'it is request.GET: ===>>> {request.GET}')
	print(f'it is id: ===>>> {id}')
	print(f'it is type id: ===>>> {type(id)}')
	return render(request, 'cars/cars_list.html', {'el': car, 'data_filter': data_filter})

# {'brands': brand},
# {'brand': model},
# {'brand': transmission},
# {'brand': region},
# {'brand': brand},
# {'brand': brand},
# {'brand': brand},
# {'brand': brand},



# class BasePage(ListView):

# model = Cars
# template_name = 'cars/base.html'
# context_object_name = 'data'
# paginate_by = 10

# def get_queryset(self):
# return Cars.objects.order_by('date_created')
# def show_page(self):
# data = Cars.objects.order_by('date_created')
# return render(self, 'cars/base.html', {'data': data})


# class CarDetailView(DetailView):

# model = Cars
# context_object_name = 'el'
# template_name = 'cars/cars_list.html'


