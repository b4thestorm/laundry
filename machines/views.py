from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import (
    api_view,
    action,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import json
from machines.models import Machine
from machines.serializers import MachineSerializer
from machines.serializers import RegistrationSerializer, TokenOverrideAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


@api_view(["GET"])
@authentication_classes([])
def machine_collection(request):
    if request.method == "GET":
        machines = Machine.objects.all()
        serializer = MachineSerializer(machines, many=True)

        return Response(serializer.data)


@api_view(["Post"])
def save_push_token(request):
    token = request.GET["token"]
    push_token = request.data["push_token"]
    user = Token.objects.get(key=token).user
    if user.push_token is not None:
        user.push_token = push_token
        user.save()

    return Response("200 OK")


@api_view(["Post"])
@authentication_classes([])
def set_machine_usage(request):
    if not request.data["minutes_remaining"]:
        return None

    if request.method == "POST":
        minutes = request.data["minutes_remaining"]
        number_of_machines = request.data["number_of_machines"]
        machine_type = request.data["machine_type"]
        token = request.data["token"]

        user = Token.objects.get(key=token).user
        available_machines = Machine.objects.create(
            minutes=minutes,
            number_of_machines=number_of_machines,
            machine_type=machine_type,
            user=user,
        )

        serializer = MachineSerializer(available_machines)

        return Response(serializer.data)


@api_view(["GET"])
def machines_remaining(request):
    available_machines = Machine.machines_remaining()
    return JsonResponse(available_machines)


@api_view(["GET"])
def set_expired(request):
    id = request.GET["id"]
    machine_to_expire = Machine.objects.get(id=id)
    machine_to_expire.set_expired()
    return Response("200 OK")


@api_view(["POST"])
@authentication_classes([])
def registration_view(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user)
            data["response"] = "successfully registered a new user."
            data["email"] = user.email
            data["token"] = token.pk
        else:
            data = serializer.errors
        return Response(data)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user, dump = TokenOverrideAuthentication.authenticate("", request)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})
