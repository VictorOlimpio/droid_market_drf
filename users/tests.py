from rest_framework.test import APITestCase
from model_bakery import baker
from faker import Factory
from django.contrib.auth.models import User as AdminUser
from users.models import User, UserProfile
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from users.views import UserViewSet

faker = Factory.create()


class UserTests(APITestCase):
    def setUp(self):
        self.users = baker.make(User, username=faker.name(), _quantity=2)
        self.factory = APIRequestFactory()
        self.user = baker.prepare(User, username=faker.name())
        profile = baker.prepare(UserProfile)
        self.user.profile = profile
        self.user.save()
        profile.user = self.user
        profile.save()
        self.admin_user = AdminUser(
            username='admin', email='admin@email.com', password='12345678', is_staff=True)
        self.url = reverse('user-list')
        self.user_data = {'profile': {'phone': '954678910'}}

    def test_get_users_without_authenticated_user(self):
        request = self.factory.get(self.url)
        view = UserViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_users_with_unauthorized_user(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        view = UserViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_users_with_authenticated_adim_user(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.admin_user)
        view = UserViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user_with_non_admin_user(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        view = UserViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.users[0].id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_logged_in_user_information(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        view = UserViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_logged_in_user_information(self):
        phone_before = self.user.profile.phone
        request = self.factory.patch(
            self.url, self.user_data, format='json')
        force_authenticate(request, user=self.user)
        view = UserViewSet.as_view({'patch': 'partial_update'})
        response = view(request, pk=self.user.id)
        phone_after = User.objects.filter(id=self.user.id)[0].profile.phone
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(phone_before, phone_after)

    def test_edit_user_with_unauthorized_user(self):
        phone_before = self.user.profile.phone
        request = self.factory.patch(
            self.url, self.user_data, format='json')
        force_authenticate(request, user=self.users[0])
        view = UserViewSet.as_view({'patch': 'partial_update'})
        response = view(request, pk=self.user.id)
        phone_after = User.objects.filter(id=self.user.id)[0].profile.phone
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(phone_before, phone_after)

    def test_edit_user_with_admin_user(self):
        phone_before = self.user.profile.phone
        request = self.factory.patch(
            self.url, self.user_data, format='json')
        force_authenticate(request, user=self.admin_user)
        view = UserViewSet.as_view({'patch': 'partial_update'})
        response = view(request, pk=self.user.id)
        phone_after = User.objects.filter(id=self.user.id)[0].profile.phone
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(phone_before, phone_after)

    def test_destroy_user_with_unauthorized_user(self):
        request = self.factory.delete(self.url)
        force_authenticate(request, user=self.user)
        view = UserViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.users[0].id)
        users_count = len(User.objects.all())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(users_count, 3)

    def test_destroy_user_with_admin_user(self):
        request = self.factory.delete(self.url)
        force_authenticate(request, user=self.admin_user)
        view = UserViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.users[0].id)
        users_count = len(User.objects.all())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(users_count, 2)
