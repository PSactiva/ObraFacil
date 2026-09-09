from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok", "app": "ObraFácil"})


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    username = str(request.data.get("username", "")).strip()
    password = request.data.get("password", "")
    password_confirmation = request.data.get("password_confirmation", "")

    if not username:
        return Response({"username": ["Informe um nome de usuário."]}, status=status.HTTP_400_BAD_REQUEST)
    if len(username) > 150:
        return Response({"username": ["O nome de usuário deve ter no máximo 150 caracteres."]}, status=status.HTTP_400_BAD_REQUEST)
    if get_user_model().objects.filter(username=username).exists():
        return Response({"username": ["Este nome de usuário já está em uso."]}, status=status.HTTP_400_BAD_REQUEST)
    if password != password_confirmation:
        return Response({"password_confirmation": ["As senhas não coincidem."]}, status=status.HTTP_400_BAD_REQUEST)

    user = get_user_model()(username=username)
    try:
        validate_password(password, user)
    except ValidationError as error:
        return Response({"password": list(error.messages)}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(password)
    user.save()
    return Response({"id": user.id, "username": user.username}, status=status.HTTP_201_CREATED)
