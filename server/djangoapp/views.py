from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from . import restapis
import json


def _body(request):
    try:
        return json.loads(request.body or b'{}')
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}


@csrf_exempt
def login_user(request):
    data = _body(request)
    username = data.get('userName') or data.get('username') or request.POST.get('username', '')
    password = data.get('password') or request.POST.get('password', '')
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({'userName': username, 'status': 'Invalid credentials'}, status=401)
    login(request, user)
    return JsonResponse({'userName': username, 'firstName': user.first_name, 'lastName': user.last_name, 'status': 'Authenticated'})


def logout_user(request):
    logout(request)
    return JsonResponse({'userName': ''})


@csrf_exempt
def registration(request):
    data = _body(request)
    username = data.get('userName') or data.get('username')
    password = data.get('password')
    if not username or not password:
        return JsonResponse({'status': 'Username and password are required'}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({'status': 'Username already exists'}, status=409)
    user = User.objects.create_user(username=username, password=password, first_name=data.get('firstName', ''), last_name=data.get('lastName', ''), email=data.get('email', ''))
    return JsonResponse({'status': 'Registered', 'userName': user.username}, status=201)


def get_dealerships(request):
    return JsonResponse({'status': 200, 'dealers': restapis.get_request('fetchDealers')})


def get_dealerships_by_state(request, state):
    return JsonResponse({'status': 200, 'dealers': restapis.get_request(f'fetchDealers/{state}')})


def get_dealer_reviews(request, dealer_id):
    reviews = restapis.get_request(f'fetchReviews/dealer/{dealer_id}')
    for review in reviews:
        review['sentiment'] = restapis.analyze_review_sentiments(review.get('review', ''))
    return JsonResponse({'status': 200, 'reviews': reviews})


def get_dealer_details(request, dealer_id):
    return JsonResponse({'status': 200, 'dealer': restapis.get_request(f'fetchDealer/{dealer_id}')})


@csrf_exempt
def add_review(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'POST required'}, status=405)
    data = _body(request)
    required = ('name', 'dealership', 'review', 'purchase_date', 'car_make', 'car_model', 'car_year')
    if any(not data.get(key) for key in required):
        return JsonResponse({'status': 'All review fields are required'}, status=400)
    data['car_year'] = int(data['car_year'])
    data.setdefault('purchase', True)
    restapis.post_review(data)
    return JsonResponse({'status': 200, 'message': 'Review submitted'})


def get_cars(request):
    rows = [{'CarMake': model.car_make.name, 'CarModel': model.name, 'CarYear': model.year} for model in CarModel.objects.select_related('car_make').all().order_by('car_make__name', 'name')]
    return JsonResponse({'CarModels': rows})


def get_all_car_makes(request):
    rows = [{'id': make.id, 'name': make.name, 'description': make.description} for make in CarMake.objects.all().order_by('name')]
    return JsonResponse({'CarMakes': rows})

