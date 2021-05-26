from django.core.management.base import BaseCommand, CommandError
from cars.models import Cars
import re
import datetime
import requests
from django.utils import timezone
import json.decoder
import logging.config
from .logging_configuration import LOGGING
logging.config.dictConfig(LOGGING)
logger = logging.getLogger('parse')
logger.info('Logger was created. Script was started')
timezone.now()
URL = 'https://auto.ria.com/api/search/auto?indexName=auto&category_id=1&marka_id%5B0%5D=55&model_id%5B0%5D=0' \
      '&abroad=2&custom=1&page=1&countpage=20&with_feedback_form=1&withOrderAutoInformer=1&with_last_id=1'
URL_CURRENT_CAR = 'https://auto.ria.com/uk/bu/blocks/json/2999/299858/29985840?langId=4&lang_id=4'
re_ex = r'\d{8}'


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('Pages')

    def handle(self, *args, **options):

        def save_data_to_db(data_car):
            try:
                car = Cars(
                    id=data_car['id'],
                    brand=data_car['brand'],
                    model=data_car['model'],
                    version=data_car['version'],
                    year=data_car['year'],
                    price_usd=data_car['price_usd'],
                    price_uah=data_car['price_uah'],
                    race=data_car['race'],
                    transmission=data_car['transmission'],
                    region=data_car['region'],
                    city=data_car['city'],
                    engine_type=data_car['engine_type'],
                    engine_capacity=data_car['engine_capacity'],
                    plate_number=data_car['plate_number'],
                    vin_code=data_car['vin_code'],
                    type_of_transport=data_car['type_of_transport'],
                    body_type=data_car['body_type'],
                    drive_type=data_car['drive_type'],
                    description=data_car['description'],
                    date_created=datetime.datetime.strptime(data_car['date_created'], "%Y-%m-%d %H:%M:%S"),
                    photo_card=data_car["photo_card"],
                    photo_view=data_car["photo_view"]
                    )

                car.save()
                logger.info(f'Data car with id {data_car["id"]} was successfully save in DB')
            except Exception:
                car = Cars.objects.filter(pk=data_car['id']).update(
                    brand=data_car['brand'],
                    model=data_car['model'],
                    version=data_car['version'],
                    year=data_car['year'],
                    price_usd=data_car['price_usd'],
                    price_uah=data_car['price_uah'],
                    race=data_car['race'],
                    transmission=data_car['transmission'],
                    region=data_car['region'],
                    city=data_car['city'],
                    engine_type=data_car['engine_type'],
                    engine_capacity=data_car['engine_capacity'],
                    plate_number=data_car['plate_number'],
                    vin_code=data_car['vin_code'],
                    type_of_transport=data_car['type_of_transport'],
                    body_type=data_car['body_type'],
                    drive_type=data_car['drive_type'],
                    description=data_car['description'],
                    date_created=datetime.datetime.strptime(data_car['date_created'], "%Y-%m-%d %H:%M:%S"),
                    photo_card=data_car["photo_card"],
                    photo_view=data_car["photo_view"]
                )
                logger.info(f'Car with id {data_car["id"]} was successfully update')

        def check_correct_data(lst_dict):
            lst_dict['autoData']['categoryId'] = 'Легкові'
            if lst_dict.get("addDate", 'Undefined value') == 'Undefined value':
                lst_dict["addDate"] = str(datetime.datetime.now())
            if lst_dict['autoData'].get('fuelName', 'Undefined value').strip().isalpha():
                lst_dict['autoData']['fuelName'] = [lst_dict['autoData']['fuelName'], 0.0]
            elif lst_dict['autoData'].get('fuelName', 'Undefined value').strip() == 'Газ / Бензин':
                lst_dict['autoData']['fuelName'] = [lst_dict['autoData']['fuelName'], 0.0]
            elif lst_dict['autoData'].get('fuelName', 'Undefined value').strip() == 'Газ метан':
                lst_dict['autoData']['fuelName'] = [lst_dict['autoData']['fuelName'], 0.0]
            elif lst_dict['autoData'].get('fuelName', 'Undefined value').strip() == 'Газ пропан-бутан':
                lst_dict['autoData']['fuelName'] = [lst_dict['autoData']['fuelName'], 0.0]
            elif lst_dict['autoData'].get('fuelName', 'Undefined value').strip() == 'Не вказано':
                lst_dict['autoData']['fuelName'] = ['Не вказано', 0.0]
            else:
                if len(lst_dict['autoData']['fuelName'].split(',')) > 1:
                    lst_dict['autoData']['fuelName'] = lst_dict['autoData']['fuelName'].split(',')
                    lst_dict['autoData']['fuelName'][1] = lst_dict['autoData']['fuelName'][1].replace('л.', '')
                    lst_dict['autoData']['fuelName'][1] = lst_dict['autoData']['fuelName'][1].replace(',', '.')
                    lst_dict['autoData']['fuelName'][1] = lst_dict['autoData']['fuelName'][1].strip()
                    lst_dict['autoData']['fuelName'][1] = float(lst_dict['autoData']['fuelName'][1])
                else:
                    lst_dict['autoData']['fuelName'] = ['Не вказано', lst_dict['autoData']['fuelName']]
                    lst_dict['autoData']['fuelName'][1] = lst_dict['autoData']['fuelName'][1].replace('л.', '')
                    lst_dict['autoData']['fuelName'][1] = lst_dict['autoData']['fuelName'][1].replace(',', '.')
                    lst_dict['autoData']['fuelName'][1] = lst_dict['autoData']['fuelName'][1].strip()
                    lst_dict['autoData']['fuelName'][1] = float(lst_dict['autoData']['fuelName'][1])

        def get_data_all_cars(ids, url):
            logger.info('Try to get data all cars')
            for id_ in ids:
                counter_cars = 1
                our_url = url.replace(re.search(re_ex, url).group(0), id_)
                try:
                    json_data = requests.get(our_url).json()
                except json.decoder.JSONDecodeError:
                    logger.info('It car id was not correct! Continue')
                    continue
                check_correct_data(json_data)
                logger.info(f'Parse data car with id:{id_}')
                data_car = ({
                    "brand": json_data.get("markName", 'Undefined value').strip(),
                    "model": json_data.get("modelName", 'Undefined value').strip(),
                    "version": json_data['autoData'].get("version", 'Undefined value').strip(),
                    "year": json_data['autoData'].get("year", 'Undefined value'),
                    "price_usd": str(json_data.get("USD", 'Undefined value')),
                    "price_uah": str(json_data.get("UAH", 'Undefined value')),
                    "race": json_data['autoData'].get("race", 'Undefined value').strip(),
                    "transmission": json_data['autoData'].get("gearboxName", 'Undefined value').strip(),
                    "region": json_data['stateData'].get('name', 'Undefined value').strip(),
                    "city": json_data.get("cityLocative", 'Undefined value').strip(),
                    "engine_type": json_data['autoData'].get("fuelName", 'Undefined value')[0].strip(),
                    "engine_capacity": json_data['autoData'].get("fuelName", 'Undefined value')[-1],
                    "plate_number": json_data.get("plateNumber", 'Undefined value').strip(),
                    "vin_code": json_data.get("VIN", 'Undefined value').strip(),
                    "type_of_transport": json_data['autoData'].get("categoryId", 'Undefined value').strip(),
                    "body_type": json_data.get("subCategoryName", 'Undefined value').strip(),
                    "drive_type": json_data["autoData"].get("driveName", 'Undefined value').strip(),
                    "description": json_data["autoData"].get("description", 'Undefined value'),
                    "date_created": json_data.get("addDate", 'Undefined value'),
                    "photo_card": json_data["photoData"].get('seoLinkB', 'https://dummyimage.com/160'),
                    "photo_view": json_data['photoData'].get('seoLinkF', 'https://dummyimage.com/360'),
                    "id": id_
                })
                logger.info(f'Try to save data car with id {id_}')
                save_data_to_db(data_car)
            print('Successful finished')

        def get_ids_and_pages(url, params=None):
            logger.info('Send get request to url...')
            json_var = requests.get(url, params=params).json()
            ids = []
            if (json_var["result"]["search_result"]["count"]) % 20 == 0:
                num_of_pages = ((json_var["result"]["search_result"]["count"]) // 20) - 1
            else:
                num_of_pages = ((json_var["result"]["search_result"]["count"]) // 20)
            if num_of_pages > 0:
                if int(options["Pages"]) < num_of_pages:
                    for page in range(int(options["Pages"])):
                        logger.info(f'Parse ids on page {page + 1}/{int(options["Pages"])}...')
                        json_var = requests.get(url).json()
                        ids.extend(json_var["result"]["search_result"]["ids"])
                        url = url.replace(f'page={page}', f'page={page + 1}')
                else:
                    for page in range(num_of_pages + 1):
                        logger.info(f'Parse ids on page {page + 1}/{int(options["Pages"])}...')
                        json_var = requests.get(url).json()
                        ids.extend(json_var["result"]["search_result"]["ids"])
                        url = url.replace(f'page={page}', f'page={page + 1}')
            else:
                logger.info(f'Parse ids on page 1/{int(options["Pages"])}...')
                ids.extend(json_var["result"]["search_result"]["ids"])
            return ids

        get_data_all_cars(get_ids_and_pages(URL), URL_CURRENT_CAR)
