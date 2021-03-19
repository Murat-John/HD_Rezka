from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from account.tasks import send_activation_code

from main.serializers import FavoriteSerializer, LikeSerializer, HistorySerializer

MyUser = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirm = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = MyUser
        fields = ('email', 'username', 'password', 'password_confirm')

    def validate(self, validate_data):
        password = validate_data.get('password')
        password_confirm = validate_data.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Password do not match')
        return validate_data

    def create(self, validate_data):
        email = validate_data.get('email')
        username = validate_data.get('username')
        password = validate_data.get('password')
        user = MyUser.objects.create_user(email=email, username=username, password=password)
        send_activation_code.delay(email=str(user.email), activation_code=str(user.activation_code))
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(label="Password",
                                     style={"input_type": "password"},
                                     trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                message = "Unable to log in with provided credentials"
                raise serializers.ValidationError(message, code='authorization')
        else:
            message = "Must include 'email' and 'password'."
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email', 'username',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        action = self.context.get('action')
        if action == 'retrieve':
            representation['favorites'] = FavoriteSerializer(instance.favorites.filter(favorite=True),
                                                             many=True, context=self.context).data
            representation['likes'] = LikeSerializer(instance.likes.filter(like=True),
                                                     many=True, context=self.context).data
            self.context['action'] = action
            representation['history'] = HistorySerializer(instance.histories.all(), many=True, context=self.context).data
        return representation

