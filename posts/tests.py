from django.test import TestCase
from django.contrib.auth import get_user_model # for the user
from . models import MissingPerson
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.

class MissingPersonModelTest(TestCase): # test the missing person model
    """Test the data creation of the missing person model"""
    def setUp(self): # User creation
        self.user = get_user_model().objects.create_user(
            username = 'Denzel Testing',
            password = 'denzel123'
        )
    
    def test_missing_person_creation(self):
        missing_person = MissingPerson.objects.create(
            user = self.user,
            name = 'Zippy',
            description = 'alipotea apo kwa gate',
            photo = SimpleUploadedFile('test.jpg', b"file_content", content_type='image/jpeg'),
            location = 'Cheptulu',
            date_missing = '2022-01-01'
        )
        # Affirm that the missing_person has been created successfully
        self.assertEqual(MissingPerson.objects.count(), 1)
    
    def test_missing_person_str_method(self): # test the string method
        """Test the string method of the missing person"""
        missing_person = MissingPerson.objects.create(
            user=self.user,
            name='Juma',
            description='Aliibiwa',
            photo=SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg"),
            location='Kaimosi',
            date_missing='2022-01-02',
        )

        # Test the __str__ method returns the expected string
        self.assertEqual(str(missing_person), 'Juma')
    
