from django.test import TestCase
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# Create your tests here.
from freelancers.models import Skill
from freelancers.models import Profile

class ProfileViews(TestCase):
    def test_index(self):
        response = self.client.get('/')
        user = auth.get_user(self.client)

        # if user.is_authenticated():
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Homepage' in response.context)
        # else:
        #    self.assertEqual(response.status_code, 302)

    def test_add_profile(self):
        response = self.client.get('/add_profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)

    def test_update_profile(self):
        response = self.client.get('/update_profile/1/')
        user = auth.get_user(self.client)

        if user.is_authenticated():
            self.assertEqual(response.status_code, 302)
        else:
            User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
            user = authenticate(username='john', password='johnpassword')
            if user.is_authenticated():
                self.assertTrue('form' in response.context)
            else:
                self.assertEqual(response.status_code, 302)
