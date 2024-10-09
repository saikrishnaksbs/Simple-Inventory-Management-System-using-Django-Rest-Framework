from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserDetailView,
    ItemListView,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
    ItemDetailView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('user/', UserDetailView.as_view(), name='user_detail'),
    path('items/', ItemListView.as_view(), name='item_list'),
    path('items/create/', ItemCreateView.as_view(), name='item_create'),
    path('items/update/<int:pk>/', ItemUpdateView.as_view(), name='item_update'),
    path('items/delete/<int:pk>/', ItemDeleteView.as_view(), name='item_delete'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item_detail'),  # New endpoint for item detail
    path('token/manual/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
