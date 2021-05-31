from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import render
import logging.config
from .logging_conf import LOGGING
from .models import Cars

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('views')

data_brand = set()
data_model = set()
data_transmission = set()
data_region = set()
data_city = set()
data_engine_type = set()
data_drive_type = set()
data_year = set()
data_engine_capacity = set()
data_body_type = set()

for obj in Cars.objects.all():
	data_brand.add(obj.brand)
	data_model.add(obj.model)
	data_transmission.add(obj.transmission)
	data_region.add(obj.region)
	data_city.add(obj.city)
	data_engine_type.add(obj.engine_type)
	data_body_type.add(obj.body_type)
	data_drive_type.add(obj.drive_type)
	data_year.add(obj.year)
	data_engine_capacity.add(obj.engine_capacity)

data_filter = {'brand': data_brand,
               'model': sorted(data_model),
               'transmission': data_transmission,
               'region': sorted(data_region),
               'city': sorted(data_city),
               'engine_type': data_engine_type,
               'body_type': data_body_type,
               'drive_type': data_drive_type,
               'year': sorted(data_year),
               'engine_capacity': sorted(data_engine_capacity)}

logger.info(f'data_filter = {data_filter}')


def filters(request):

	logger.info('filter def')
	full_path = HttpRequest.get_full_path(request)
	request_get = request.GET
	filter = Cars.objects.all()
	for param in request_get:
		if param == 'price_from' and request_get.get(param) != '':
			logger.info('Условие price_from СРАБОТАЛО!')
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
			if request_get.get(param) != '':
				filter = filter.filter(year=request_get.get(param))
			else:
				filter = filter.filter(year=None)
			continue
		elif param == 'region':
			filter = filter.filter(region=request_get.get(param))
			continue
		elif param == 'city':
			filter = filter.filter(city=request_get.get(param))
			continue
		elif param == 'engine_capacity':
			if request_get.get(param) != '':
				filter = filter.filter(engine_capacity=request_get.get(param))
			else:
				filter = filter.filter(engine_capacity=None)
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

		logger.info(param)
		logger.info(type(param))

	logger.info(filter)
	paginator_f = Paginator(filter, 20)
	page_number = request.GET.get('page')
	page_obj_1 = paginator_f.get_page(page_number)

	return render(request, 'cars/base.html', {'data': page_obj_1.object_list,
	                                          'data_filter': data_filter,
	                                          'page_obj': page_obj_1,
	                                          'request': request_get,
	                                          'full_path': full_path})


def base_page(request):

	logger.info('base_page def')
	logger.info(f'REQUEST IS {request}')
	logger.info(f'REQUEST IS {request.GET}')
	full_path = HttpRequest.get_full_path(request)
	logger.info(f'full_path {full_path}')
	data = Cars.objects.order_by('date_created')
	paginator = Paginator(data, 20)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)  # Ссылка на конкретную страницу пагинатора
	for i in data_filter:
		if request.GET.get(i):
			logger.info('filter def get(i)')
			return filters(request)
	if (request.GET.get('price_from') not in ('', None)) or (request.GET.get('price_to') not in ('', None)):
		logger.info('filter def price')
		logger.info(request.GET.get('price_from'))
		logger.info(request.GET.get('price_to '))
		return filters(request)
	else:
		return render(request, 'cars/base.html', {
			'data': page_obj.object_list,
			'page_obj': page_obj,
			'data_filter': data_filter,
			'request': request.GET,
			'full_path': full_path})


def detail_car(request, id):
	logger.info('detail_car def')
	car = Cars.objects.get(pk=id)
	logger.info(f'it is request: ===>>> {request}')
	logger.info(f'it is type request: ===>>> {type(request)}')
	logger.info(f'it is request.GET: ===>>> {request.GET}')
	logger.info(f'it is id: ===>>> {id}')
	logger.info(f'it is type id: ===>>> {type(id)}')
	return render(request, 'cars/cars_list.html', {'el': car, 'data_filter': data_filter})

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
