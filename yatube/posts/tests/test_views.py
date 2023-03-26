from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django import forms

from ..models import Group, Post

User = get_user_model()


class PostPagesTests(TestCase):
    NUM_OS_POSTS = 13

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )
        Post.objects.bulk_create([Post(text=f'text_post_{i}', author=cls.user)
                                 for i in range(1, cls.NUM_OS_POSTS + 1)])

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем используемые шаблоны
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': 'test-slug'}): 'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': 'auth'}): 'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': '5'}): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit', kwargs={'post_id': '5'}): 'posts/create_post.html',
        }

        for reverse_name, template in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_context_index(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        obj = response.context['page_obj']
        first_post = obj[0]
        self.assertEqual(len(obj), 10)
        self.assertEqual(first_post, self.post)
        self.assertEqual(first_post.text, 'Тестовый пост')
        self.assertEqual(first_post.author.username, 'auth')

    def test_context_group_list(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:group_list', kwargs={'slug': 'test-slug'}))
        obj = response.context['page_obj']

        self.assertEqual(len(obj), 10)


    # def test_context_profile(self):
    #     """Шаблон index сформирован с правильным контекстом."""
    #     response = self.authorized_client.get(reverse('posts:index'))
    #     self.assertEqual(response.context['page_obj'][0].id, self.post.id)
    #     self.assertEqual(response.context['group'], self.group)

    # def test_context_post_detail(self):
    #     """Шаблон index сформирован с правильным контекстом."""
    #     response = self.authorized_client.get(reverse('posts:index'))
    #     obj = response.context['page_obj']
    #     self.assertEqual(obj[0].id, self.post.id)
    #
    # def test_context_create_post(self):
    #     """Шаблон index сформирован с правильным контекстом."""
    #     response = self.authorized_client.get(reverse('posts:index'))
    #     obj = response.context['page_obj']
    #     self.assertEqual(obj[0].id, self.post.id)
    #
    # def test_context_post_edit(self):
    #     """Шаблон index сформирован с правильным контекстом."""
    #     response = self.authorized_client.get(reverse('posts:index'))
    #     obj = response.context['page_obj']
    #     self.assertEqual(obj[0].id, self.post.id)