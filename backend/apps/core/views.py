from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok", "app": "ObraFácil"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    return Response({"id": request.user.id, "username": request.user.username})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    Token.objects.filter(user=request.user).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([AllowAny])
def request_password_reset(request):
    email = str(request.data.get("email", "")).strip().lower()
    user = get_user_model().objects.filter(email__iexact=email, is_active=True).first()
    if user and user.email:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        reset_url = f"{settings.FRONTEND_URL.rstrip('/')}/?uid={uid}&token={token}"
        send_mail(
            "Recuperação de acesso - ObraFácil",
            f"Olá, {user.username}. Seu usuário é {user.username}. Acesse este link para criar uma nova senha: {reset_url}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
    return Response({"detail": "Se o e-mail estiver cadastrado, enviaremos as instruções de recuperação."})


@api_view(["POST"])
@permission_classes([AllowAny])
def confirm_password_reset(request):
    uid = request.data.get("uid", "")
    token = request.data.get("token", "")
    password = request.data.get("password", "")
    password_confirmation = request.data.get("password_confirmation", "")
    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = get_user_model().objects.get(pk=user_id, is_active=True)
    except (TypeError, ValueError, OverflowError, ValidationError, get_user_model().DoesNotExist):
        user = None

    if not user or not PasswordResetTokenGenerator().check_token(user, token):
        return Response({"detail": ["O link de recuperação é inválido ou expirou."]}, status=status.HTTP_400_BAD_REQUEST)
    if password != password_confirmation:
        return Response({"password_confirmation": ["As senhas não coincidem."]}, status=status.HTTP_400_BAD_REQUEST)
    try:
        validate_password(password, user)
    except ValidationError as error:
        return Response({"password": list(error.messages)}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(password)
    user.save(update_fields=["password"])
    Token.objects.filter(user=user).delete()
    return Response({"detail": "Senha redefinida com sucesso."})


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    username = str(request.data.get("username", "")).strip()
    password = request.data.get("password", "")
    password_confirmation = request.data.get("password_confirmation", "")
    email = str(request.data.get("email", "")).strip().lower()

    if not username:
        return Response({"username": ["Informe um nome de usuário."]}, status=status.HTTP_400_BAD_REQUEST)
    if len(username) > 150:
        return Response({"username": ["O nome de usuário deve ter no máximo 150 caracteres."]}, status=status.HTTP_400_BAD_REQUEST)
    if get_user_model().objects.filter(username=username).exists():
        return Response({"username": ["Este nome de usuário já está em uso."]}, status=status.HTTP_400_BAD_REQUEST)
    if not email:
        return Response({"email": ["Informe um e-mail para recuperação de acesso."]}, status=status.HTTP_400_BAD_REQUEST)
    try:
        validate_email(email)
    except ValidationError:
        return Response({"email": ["Informe um e-mail válido."]}, status=status.HTTP_400_BAD_REQUEST)
    if get_user_model().objects.filter(email__iexact=email).exists():
        return Response({"email": ["Este e-mail já está em uso."]}, status=status.HTTP_400_BAD_REQUEST)
    if password != password_confirmation:
        return Response({"password_confirmation": ["As senhas não coincidem."]}, status=status.HTTP_400_BAD_REQUEST)

    user = get_user_model()(username=username, email=email)
    try:
        validate_password(password, user)
    except ValidationError as error:
        return Response({"password": list(error.messages)}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(password)
    user.save()
    return Response({"id": user.id, "username": user.username}, status=status.HTTP_201_CREATED)
