from django.shortcuts import render

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.permissions import IsAuthorOrReadOnly
from .serializers import (
    CollectSerializer, CollectCreateSerializer,
    PaymentSerializer, PaymentCreateSerializer,
    UserSerializer
)
from payment.models import Payment
from collect.models import Collect

from .tasks import send_collect_created_email, send_payment_notification


class CollectViewSet(viewsets.ModelViewSet):
    queryset = Collect.objects.all().select_related('author').prefetch_related('payments__donor')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return CollectCreateSerializer
        return CollectSerializer

    def perform_create(self, serializer):
        collect = serializer.save(author=self.request.user)
        send_collect_created_email.delay_on_commit(collect.id)

    @action(detail=True, methods=['get'])
    def payments(self, request, pk=None):
        collect = get_object_or_404(Collect, pk=pk)
        payments = collect.payments.all().select_related('donor')
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().select_related('donor', 'collect')
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

    def perform_create(self, serializer):
        payment = serializer.save(donor=self.request.user)
        send_payment_notification.delay_on_commit(payment.id)
