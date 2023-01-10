from . import models, views, admin, forms
from django.test import TestCase, tag, Client
from django.urls import reverse
from django.core import mail
from django.http import HttpRequest, HttpResponse,response,request
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,get_user_model,get_user,user_logged_in

#Create your tests here.

class SigninTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com')
        self.user.save()
        self.user = get_user_model().objects.create_user(username='Oncologist', password='12test12', email='Oncologist@example.com')
        self.user.save()

    def test_correct(self):
        user1 = authenticate(username='test', password='12test12')
        self.assertTrue((user1 is not None) and user1.is_authenticated)
        user2 = authenticate(username='Oncologist', password='12test12')
        self.assertTrue((user2 is not None) and user2.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)

    def tearDown(self):
        self.user.delete()


class LoginTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)


    def test_login(self):
        # send login data
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)

class AdminSiteTests(TestCase):
   
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='testuser', password='testpass', email='test@example.com')
        self.client.login(username='testuser', password='testpass')

        # create a regular user for testing
        self.user = User.objects.create_user(username='testuser2', password='testpass2', email='test2@example.com',id=50)
    def test_change_user_fields(self):
        
        # send a request to the Django admin change form for the user
        response = self.client.get(f'/admin/auth/user/{50}/change/')
        self.assertEqual(response.status_code, 200)  # Check that the response is successful