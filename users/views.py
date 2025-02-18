from django.shortcuts import render
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.create_user(username=['username'],password=data['password'])
        return JsonResponse({'message':'User registered Successfully'})

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(username=['username'], password=['password'])
        if user:
            login(request,user)
            return JsonResponse({'message': 'Login Successful'})
        else:
            return JsonResponse({'message':'Invalid Credentials'})
