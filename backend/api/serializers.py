
from rest_framework import serializers
from django.contrib.auth.models import User

from payment.models import Payment
from collect.models import Collect

from .helpers import Base64ImageField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class PaymentSerializer(serializers.ModelSerializer):
    donor = UserSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'collect', 'donor', 'amount', 'created_at']
        read_only_fields = ['id', 'created_at']


class CollectSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Collect
        fields = [
            'id', 'author', 'title', 'reason', 'description',
            'target_amount', 'collected_amount', 'donors_count',
            'image', 'created_at', 'ends_at', 'payments'
        ]
        read_only_fields = ['id', 'collected_amount', 'donors_count', 'created_at']


class CollectCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Collect
        fields = [
            'title', 'reason', 'description',
            'target_amount', 'image', 'ends_at'
        ]
        read_only_fields = ['id']

    def validate_target_amount(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError(
                "Сумма должна быть положительной или null (для безлимитного сбора)."
            )
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super().create(validated_data)


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'collect', 'amount', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Сумма платежа должна быть положительной")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['donor'] = request.user
        return super().create(validated_data)