import json
from pathlib import Path
from django.contrib.auth.models import User
from .models import CarMake, CarModel


def initiate():
    data_file = Path(__file__).resolve().parent.parent / 'database' / 'data' / 'car_records.json'
    cars = json.loads(data_file.read_text(encoding='utf-8'))['cars']
    for car in cars:
        make, _ = CarMake.objects.get_or_create(name=car['make'], defaults={'description': f'{car["make"]} vehicles'})
        body = str(car.get('bodyType', 'Sedan')).upper()
        body = body if body in {'SEDAN', 'SUV', 'WAGON', 'COUPE'} else 'SEDAN'
        year = max(2015, min(2026, int(car.get('year', 2023))))
        CarModel.objects.get_or_create(car_make=make, name=car['model'], defaults={'type': body.title() if body != 'SUV' else 'SUV', 'year': year})
    if not User.objects.filter(username='root').exists():
        User.objects.create_superuser('root', 'root@example.com', 'RootPass123!')
