from rest_framework import serializers, authentication, exceptions
from machines.models import Machine, CustomUser


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ("id", "minutes", "number_of_machines", "machine_type", "user")


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    auth_token = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "password2", "auth_token", "push_token"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        user = CustomUser(email=self.validated_data["email"])
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        push_token = self.validated_data["push_token"]
        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})

        user.set_password(password)
        user.push_token = push_token
        user.save()

        return user


class TokenOverrideAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        email = request.data["email"]
        if not email:
            return None

        try:
            user = CustomUser.objects.get(email=email)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("No such user")

        return (user, None)
