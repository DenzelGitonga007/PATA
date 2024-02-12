# from django.test import TestCase
# from .models import CustomUser # for the custom user

# # Create your tests here.
# class CustomUserModelTest(TestCase):
#     """Test the user model"""
#     # Create the user
#     def setUp(self):
#         """Create the user"""
#         self.user = CustomUser.objects.create_user(
#             username = 'testuser',
#             email = 'test@gmail.com',
#             password = 'denzel123'
#         )
    
#     # Test that the user was created successfully
#     def test_user_creation(self):
#         """Test that user was created successfully"""
#         self.assertEqual(CustomUser.objects.count(), 1)
    
#     # Test the __str__ method returns the name
#     def test_user_str_method(self):
#         """Tests that the __str__ method returns the string correctly"""
#         self.assertEqual(str(self.user), 'testuser')

#     # Test the get_fullname()
#     def test_user_get_fullname(self):
#         """Test the get_fullname method"""
#         self.assertEqual(self.user.get_full_name(), 'testuser')
    
#     # Test the user_type field
#     def test_user_type(self):
#         """Test the user_type"""
#         self.assertIn(self.user.user_type, dict(CustomUser.user_type_choices).keys())
