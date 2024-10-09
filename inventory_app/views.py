from django.shortcuts import get_object_or_404, render
from django.core.cache import cache  # Import cache
from rest_framework import generics  # Import generics for better structure
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser, Item
from .serializers import CustomUserSerializer, UserLoginSerializer, ItemSerializer
from logger import logger

class UserRegistrationView(APIView):
    try:
        queryset = CustomUser.objects.all()
        serializer_class = CustomUserSerializer
        permission_classes = (AllowAny,)
    
        def post(self, request, *args, **kwargs):
            try:
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error(f'User registration failed: {e}')
                return Response({'detail': 'User registration failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error(f'User registration failed: {e}')

class UserLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
                if user is not None:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    })
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'User login failed: {e}')
            return Response({'detail': 'User login failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDetailView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            serializer = CustomUserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f'User details retrieval failed: {e}')
            return Response({'detail': 'User details retrieval failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ItemListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            items = Item.objects.all()
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f'Item list retrieval failed: {e}')
            return Response({'detail': 'Item list retrieval failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        try:
            cache_key = f'item_{pk}'
            item_data = cache.get(cache_key)

            if not item_data:
                # Cache miss, fetch from the database
                item = get_object_or_404(Item, pk=pk)
                serializer = ItemSerializer(item)
                item_data = serializer.data
                # Store the item data in Redis cache
                cache.set(cache_key, item_data, timeout=60 * 15)  # Cache for 15 minutes

            return Response(item_data)
        except Exception as e:
            logger.error(f'Item details retrieval failed: {e}')
            return Response({'detail': 'Item details retrieval failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ItemCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Item creation failed: {e}')
            return Response({'detail': 'Item creation failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ItemUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        try:
            item = get_object_or_404(Item, pk=pk)
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                # Invalidate cache for updated item
                cache.delete(f'item_{pk}')
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Item update failed: {e}')
            return Response({'detail': 'Item update failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ItemDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        try:
            item = get_object_or_404(Item, pk=pk)
            item.delete()
            # Invalidate cache for deleted item
            cache.delete(f'item_{pk}')
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f'Item deletion failed: {e}')
            return Response({'detail': 'Item deletion failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)