from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .utils import generate_otp, send_otp_email

User = get_user_model()

# Temporary in-memory OTP store
otp_storage = {}


# ==================== SIGNUP ====================
@api_view(['POST'])
def signup(request):
    email = request.data.get("email")
    username = request.data.get("username")
    password = request.data.get("password")

    if not email or not username or not password:
        return Response({"error": "Email, username and password are required."}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered."}, status=400)

    otp = generate_otp()
    otp_storage[email] = {"otp": otp, "purpose": "signup"}
    send_otp_email(email, otp, "Signup")

    return Response({"message": "OTP sent to your email for signup verification."})


@api_view(['POST'])
def verify_signup(request):
    email = request.data.get("email")
    entered_otp = request.data.get("otp")
    username = request.data.get("username")
    password = request.data.get("password")

    if not email or not entered_otp:
        return Response({"error": "Email and OTP are required."}, status=400)

    otp_data = otp_storage.get(email)
    if not otp_data or otp_data["otp"] != entered_otp or otp_data["purpose"] != "signup":
        return Response({"error": "Invalid OTP."}, status=400)

    # OTP verified → create user
    user = User.objects.create_user(username=username, email=email, password=password)
    otp_storage.pop(email, None)
    return Response({"message": "Signup successful!"})


# ==================== LOGIN ====================
@api_view(['POST'])
def login_request(request):
    email = request.data.get("email")

    if not email:
        return Response({"error": "Email required."}, status=400)

    if not User.objects.filter(email=email).exists():
        return Response({"error": "No user found with this email."}, status=404)

    otp = generate_otp()
    otp_storage[email] = {"otp": otp, "purpose": "login"}
    send_otp_email(email, otp, "Login")

    return Response({"message": "OTP sent to your email for login verification."})


@api_view(['POST'])
def verify_login_otp(request):
    email = request.data.get("email")
    entered_otp = request.data.get("otp")

    if not email or not entered_otp:
        return Response({"error": "Email and OTP are required."}, status=400)

    otp_data = otp_storage.get(email)
    if not otp_data or otp_data["otp"] != entered_otp or otp_data["purpose"] != "login":
        return Response({"error": "Invalid OTP."}, status=400)

    otp_storage.pop(email, None)
    return Response({"message": "Login successful!"})


# ==================== RESEND OTPS ====================
@api_view(['POST'])
def resend_signup_otp(request):
    email = request.data.get("email")
    if not email:
        return Response({"error": "Email required."}, status=400)

    otp = generate_otp()
    otp_storage[email] = {"otp": otp, "purpose": "signup"}
    send_otp_email(email, otp, "Signup Resend")

    return Response({"message": "Signup OTP resent to your email."})


@api_view(['POST'])
def resend_login_otp(request):
    email = request.data.get("email")
    if not email:
        return Response({"error": "Email required."}, status=400)

    otp = generate_otp()
    otp_storage[email] = {"otp": otp, "purpose": "login"}
    send_otp_email(email, otp, "Login Resend")

    return Response({"message": "Login OTP resent to your email."})


# ==================== FORGOT PASSWORD ====================
@api_view(['POST'])
def forgot_password_request(request):
    email = request.data.get("email")

    if not email:
        return Response({"error": "Email required."}, status=400)

    if not User.objects.filter(email=email).exists():
        return Response({"error": "No user found with this email."}, status=404)

    otp = generate_otp()
    otp_storage[email] = {"otp": otp, "purpose": "forgot_password"}
    send_otp_email(email, otp, "Password Reset")

    return Response({"message": "OTP sent to your email for password reset."})


@api_view(['POST'])
def verify_reset_otp(request):
    email = request.data.get("email")
    entered_otp = request.data.get("otp")

    if not email or not entered_otp:
        return Response({"error": "Email and OTP are required."}, status=400)

    otp_data = otp_storage.get(email)
    if not otp_data or otp_data["otp"] != entered_otp or otp_data["purpose"] != "forgot_password":
        return Response({"error": "Invalid OTP."}, status=400)

    otp_storage.pop(email, None)
    return Response({"message": "OTP verified. You can now reset your password."})


@api_view(['POST'])
def reset_password(request):
    email = request.data.get("email")
    new_password = request.data.get("new_password")

    if not email or not new_password:
        return Response({"error": "Email and new password required."}, status=400)

    try:
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password reset successfully."})
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)


@api_view(['POST'])
def logout(request):
    return Response({"message": "Logout endpoint"})
