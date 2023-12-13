from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import logout


SECRET_KEY='nikhil1234'
# Create your v



@csrf_exempt
def generate_token(request):
    payload = {
        'user_id': 1,
        'username': 'john_doe',
        'exp': datetime.utcnow() + timedelta(days=1) 
    }

    # Generate JWT token
    token = jwt.encode(payload,SECRET_KEY, algorithm='HS256')
    return JsonResponse({'token': token})


@csrf_exempt
def verify_token(request):
    if request.method == 'POST':
        # Extract the token from the request
        token = request.POST.get('token', None)

        if token:
            try:
                # Decode the token
                decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                return JsonResponse({'success': True, 'decoded_payload': decoded_payload})
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token has expired.'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token.'}, status=401)

    return JsonResponse({'error': 'Invalid request.'}, status=400)



@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            return redirect('dashboard')
            return JsonResponse({'status': 'success', 'message': 'Logged in'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'status': 'success', 'message': 'Logged out'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def dashboard(request):
    return render(request,'dashboard.html')
