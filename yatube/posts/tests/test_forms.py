# # deals/tests/tests_form.py
# from django.core.files.uploadedfile import SimpleUploadedFile
# from django.test import Client, TestCase
# from django.urls import reverse
#
# from ..forms import PostForm
# from ..models import Post, Group
#
#
# class TaskCreateFormTests(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         Post.objects.create(
#             text='Тестовый текст',
#         )
#
#     def setUp(self):
#         self.guest_client = Client()
#
#     def test_cant_create_existing_slug(self):
#         pass