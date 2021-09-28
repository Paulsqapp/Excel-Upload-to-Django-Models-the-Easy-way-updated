from django.test import TestCase
from .models import Staff, Sales
from django.contrib.auth.models import User

import random
# Create your tests here.

class TestCoreModels(TestCase):
    
    def setUp(self):
        user_ = User.objects.create(username='admin')
        designation_ = random.choice(['junior', 'super','manager',])
        self.data1 = Staff.objects.create(
            name=user_, display_name='pk', designation=designation_)

    def test_staff_entry(self):
        data = self.data1 
        self.assertTrue(isinstance(data, Staff))
