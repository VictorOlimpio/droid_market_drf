from rest_framework.test import APITestCase
from model_bakery import baker
from faker import Factory
from django.contrib.auth.models import User as AdminUser
from users.models import User, UserProfile
from pieces.models import Piece
from demands.models import Demand
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from demands.views import DemandViewSet

faker = Factory.create()


class UserTests(APITestCase):
    def setUp(self):
        self.pieces = baker.make(Piece, _quantity=2)
        self.users = baker.make(User, username=faker.name(), _quantity=2)
        self.factory = APIRequestFactory()

        self.user = baker.prepare(User, username=faker.name())
        profile = baker.prepare(UserProfile)
        self.user.profile = profile
        self.user.save()
        profile.user = self.user
        profile.save()
        self.demand1 = baker.make(Demand, owner=self.user, piece=self.pieces[0])

        self.user2 = baker.prepare(User, username=faker.name())
        profile2 = baker.prepare(UserProfile)
        self.user2.profile = profile2
        self.user2.save()
        profile2.user = self.user2
        profile2.save()
        self.demand2 = baker.make(Demand, owner=self.user2, piece=self.pieces[1])

        self.admin_user = baker.prepare(User,
            username='admin', email='admin@email.com', password='12345678', is_superuser=True, is_staff=True)
        profile3 = baker.prepare(UserProfile)
        self.admin_user.profile = profile3
        self.admin_user.save()
        profile3.user = self.admin_user
        profile3.save()
        
        self.url = reverse('demand-list')
        self.demand_data = {
            'status': 1
        }

    def test_get_demand_without_authenticated_user(self):
        request = self.factory.get(self.url)
        view = DemandViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_demands_with_authenticated_user(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        view = DemandViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_demands_with_authenticated_adim_user(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.admin_user)
        view = DemandViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_demand_using_owner(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        view = DemandViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.demand1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_demand_not_using_owner(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        view = DemandViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.demand2.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_demand_using_owner(self):
        status_before = self.demand1.status
        request = self.factory.patch(
            self.url, self.demand_data, format='json')
        force_authenticate(request, user=self.user)
        view = DemandViewSet.as_view({'patch': 'partial_update'})
        response = view(request, pk=self.demand1.id)
        status_after = Demand.objects.filter(id=self.demand1.id)[0].status
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(status_before, status_after)

    def test_edit_demand_not_using_owner(self):
        status_before = self.demand2.status
        request = self.factory.patch(
            self.url, self.demand_data, format='json')
        force_authenticate(request, user=self.user)
        view = DemandViewSet.as_view({'patch': 'partial_update'})
        response = view(request, pk=self.demand2.id)
        status_after = Demand.objects.filter(id=self.demand2.id)[0].status
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(status_before, status_after)

    def test_edit_demand_using_admin(self):
        status_before = self.demand2.status
        request = self.factory.patch(
            self.url, self.demand_data, format='json')
        force_authenticate(request, user=self.admin_user)
        view = DemandViewSet.as_view({'patch': 'partial_update'})
        response = view(request, pk=self.demand2.id)
        status_after = Demand.objects.filter(id=self.demand2.id)[0].status
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(status_before, status_after)

    def test_destroy_demand_using_admin_user(self):
        request = self.factory.delete(self.url)
        force_authenticate(request, user=self.admin_user)
        view = DemandViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.demand1.id)
        demands_count = len(Demand.objects.all())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(demands_count, 1)

    def test_destroy_demand_using_owner(self):
        request = self.factory.delete(self.url)
        force_authenticate(request, user=self.user)
        view = DemandViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.demand1.id)
        demands_count = len(Demand.objects.all())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(demands_count, 1)

    def test_destroy_demand_not_using_owner(self):
        request = self.factory.delete(self.url)
        force_authenticate(request, user=self.user)
        view = DemandViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.demand2.id)
        demands_count = len(Demand.objects.all())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(demands_count, 2)
