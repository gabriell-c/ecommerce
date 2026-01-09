from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from drf_extra_fields.fields import Base64ImageField # Importante!

class ProfileSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=False, allow_null=True)
    class Meta:
        model = Profile
        fields = ["phone", "avatar", "birthdate", "cep", "street", "number", "city", "state"]

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "profile"]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        
        # Atualiza campos do User
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Atualiza campos do Profile
        profile = instance.profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return instance

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )

        Profile.objects.create(user=user)
        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


# ==========================
# LOGIN USANDO EMAIL (CORRIGIDO)
# ==========================
class EmailLoginTokenSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Em produção use "Credenciais inválidas", no dev use a real:
            raise AuthenticationFailed("E-mail não cadastrado.")

        if not user.check_password(password):
            raise AuthenticationFailed("Senha incorreta.")

        attrs["username"] = user.username
        return super().validate(attrs)