from json import JSONDecodeError
from django.http import JsonResponse
from .serializers import TradeSerializer, SummarySerializer
from .models import Summary , Trade
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin,UpdateModelMixin,RetrieveModelMixin, DestroyModelMixin, CreateModelMixin


class UserRegister(APIView):
    """
    For Sign-up purpose
    """
    def post(self, request):
        data = JSONParser().parse(request)
        try:
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
            )
            return Response({'message': 'Welcome!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': f'Error in registration: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


class TradeViewSet(
        ListModelMixin,
        RetrieveModelMixin,
        DestroyModelMixin,
        viewsets.GenericViewSet
        ):
    """
    A simple ViewSet for listing or creating trades.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = TradeSerializer


    def get_queryset(self):
        user = self.request.user
        return Trade.objects.filter(user=user).all()

    def create(self, request):
        try:
            data = JSONParser().parse(request)
            current_user = request.user
            serializer = self.get_serializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=current_user, summary=current_user.summary)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)

    def partial_update(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)


class SummaryViewSet(
        ListModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        viewsets.GenericViewSet
        ):
    """
    A simple ViewSet for listing, and updating balance and starting balance.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SummarySerializer

    def get_queryset(self):
        user = self.request.user
        return Summary.objects.filter(user=user).all()

    def partial_update(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)
