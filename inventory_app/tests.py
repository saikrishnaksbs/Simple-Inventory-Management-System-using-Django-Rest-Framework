import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Item
from django.core.cache import cache

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
@pytest.mark.django_db
def user():
    return User.objects.create_user(email='test@example.com', username='testuser', password='testpass')

@pytest.fixture
@pytest.mark.django_db
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.mark.django_db
class TestUserAndItemAPI:

    def test_user_registration(self, api_client):
        response = api_client.post('/inventory_app/register/', {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'newpass'})
        assert response.status_code == 201
        assert 'username' in response.data

    def test_user_detail(self, auth_client, user):
        response = auth_client.get('/inventory_app/user/')
        assert response.status_code == 200
        assert response.data['username'] == user.username

    def test_item_list(self, auth_client):
        Item.objects.create(name='Item1', description='Description1')
        response = auth_client.get('/inventory_app/items/')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_item_detail(self, auth_client):
        item = Item.objects.create(name='Item1', description='Description1')
        response = auth_client.get(f'/inventory_app/items/{item.pk}/')
        assert response.status_code == 200
        assert response.data['name'] == item.name

    def test_item_creation(self, auth_client):
        response = auth_client.post('/inventory_app/items/create/', {'name': 'NewItem', 'description': 'NewDescription'})
        assert response.status_code == 201
        assert response.data['name'] == 'NewItem'

    def test_item_update(self, auth_client):
        item = Item.objects.create(name='Item1', description='Description1')
        response = auth_client.put(f'/inventory_app/items/update/{item.pk}/', {'name': 'UpdatedItem', 'description': 'UpdatedDescription'})
        assert response.status_code == 200
        assert response.data['name'] == 'UpdatedItem'

    def test_item_delete(self, auth_client):
        item = Item.objects.create(name='Item1', description='Description1')
        response = auth_client.delete(f'/inventory_app/items/delete/{item.pk}/')
        assert response.status_code == 204
        assert Item.objects.filter(pk=item.pk).count() == 0

    def test_item_cache(self, auth_client):
        item = Item.objects.create(name='CachedItem', description='CachedDescription')
        cache_key = f'item_{item.pk}'
        response = auth_client.get(f'/inventory_app/items/{item.pk}/')
        cached_data = cache.get(cache_key)
        assert cached_data is not None  # Ensure cached_data is not None
        assert cached_data['name'] == item.name
        assert response.data['name'] == cached_data['name']
