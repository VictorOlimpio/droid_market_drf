from rest_framework.test import APITestCase
from model_bakery import baker
from faker import Factory
from django.contrib.auth.models import User as AdminUser
from users.models import User, UserProfile
from pieces.models import Piece
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from pieces.views import PieceViewSet

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
        self.admin_user = AdminUser(
            username='admin', email='admin@email.com', password='12345678', is_staff=True)
        self.url = reverse('piece-list')
        self.piece_data = {
            'description': 'a head'
        }

    def test_get_piece_without_authenticated_user(self):
        request = self.factory.get(self.url)
        view = PieceViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_pieces_with_authenticated_adim_user(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.admin_user)
        view = PieceViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_piece_with_non_admin_user(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        view = PieceViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.pieces[0].id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_piece_with_non_admin_user(self):
        piece = self.pieces[0]
        description_before = piece.description
        request = self.factory.patch(
            self.url, self.piece_data, format='json')
        force_authenticate(request, user=self.user)
        view = PieceViewSet.as_view({'patch': 'partial_update'})
        response = view(request, pk=piece.id)
        description_after = Piece.objects.filter(id=piece.id)[0].description
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(description_before, description_after)

    def test_edit_piece_with_admin_user(self):
        piece = self.pieces[0]
        description_before = piece.description
        request = self.factory.patch(
            self.url, self.piece_data, format='json')
        force_authenticate(request, user=self.admin_user)
        view = PieceViewSet.as_view({'patch': 'partial_update'})
        response = view(request, pk=piece.id)
        description_after = Piece.objects.filter(id=piece.id)[0].description
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(description_before, description_after)

    def test_destroy_piece_with_admin_user(self):
        request = self.factory.delete(self.url)
        force_authenticate(request, user=self.admin_user)
        view = PieceViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.pieces[0].id)
        pieces_count = len(Piece.objects.all())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(pieces_count, 1)

    def test_destroy_piece_with_non_admin_user(self):
        request = self.factory.delete(self.url)
        force_authenticate(request, user=self.user)
        view = PieceViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.pieces[0].id)
        pieces_count = len(Piece.objects.all())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(pieces_count, 1)
