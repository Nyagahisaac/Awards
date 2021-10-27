from django.test import TestCase
from django.test import TestCase
from .models import Profile,Reviews,Rates,Project_Post


# Create your tests here.
class ProfileTestClass(TestCase):

    def setup(self):
        self.profile = Profile(user = 'dan',profile_pic = 'd.jpg',bio ='my bio',updated_on = '12/7/1019')
        self.profile.save()
    def test_instance(self):
        self.assertTrue(isinstance(self.profile,Profile))

    def test_get_profile_by_user(self):
        profile = Profile.get_profile_by_name()
        self.assertTrue(profile == self.profile)


