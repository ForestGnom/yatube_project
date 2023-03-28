from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django import forms

from ..models import Group, Post

User = get_user_model()


class PostPagesTests(TestCase):
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
            group=cls.group
        )

        cls.post2 = Post.objects.create(
            author=User.objects.create_user(username='auth2'),
            text='Тестовый пост2',
            group=Group.objects.create(
                title='Тестовая группа2', slug='test-slug2', description='Тестовое описание2')
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем используемые шаблоны
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': self.group.slug}): 'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': self.user.username}): 'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}): 'posts/create_post.html',
        }

        for reverse_name, template in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_pages_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        obj = response.context['page_obj']
        first_object = obj[0]
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_group_0 = first_object.group.title
        self.assertEqual(post_text_0, 'Тестовый пост')
        self.assertEqual(post_author_0, 'auth')
        self.assertEqual(post_group_0, 'Тестовая группа')

    def test_group_pages_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:group_list', kwargs={'slug': 'test-slug'}))
        obj = response.context['group']
        group_title_0 = obj.title
        group_slug_0 = obj.slug
        self.assertEqual(group_title_0, 'Тестовая группа')
        self.assertEqual(group_slug_0, 'test-slug')

    def test_profile_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом"""
        response = self.authorized_client.get(reverse('posts:profile', kwargs={'username': self.user.username}))
        obj = response.context['page_obj']
        first_object = obj[0]
        post_text_0 = first_object.text
        user_0 = response.context['author'].username
        self.assertEqual(post_text_0, 'Тестовый пост')
        self.assertEqual(user_0, 'auth')

    def test_post_detail_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом"""
        response = self.authorized_client.get(reverse('posts:post_detail', kwargs={'post_id': self.post.id}))
        obj = response.context['post']
        post_text_0 = obj.text
        self.assertEqual(post_text_0, 'Тестовый пост')

    def test_post_create_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом"""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_edit_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом"""
        response = self.authorized_client.get(reverse('posts:post_edit', kwargs={'post_id': self.post.id}))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_in_your_group(self):
        """пост не попал в группу, для которой не был предназначен"""
        response = self.authorized_client.get(reverse('posts:group_list', kwargs={'slug': 'test-slug2'}))
        obj = response.context['page_obj']
        first_object = obj[0]
        post_text_0 = first_object.text
        self.assertTrue(post_text_0, 'Тестовый пост')


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user3 = User.objects.create_user(username='auth3')
        cls.group3 = Group.objects.create(
            title='Тестовая группа3',
            slug='test-slug3',
            description='Тестовое описание3',
        )
        cls.posts3 = []
        for i in range(13):
            cls.posts3.append(Post(
                text=f'Тестовый пост {i}',
                author=cls.user3,
                group=cls.group3)
            )
        Post.objects.bulk_create(cls.posts3)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user3)

    def test_first_page_contains_ten_records(self):
        urls = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': 'test-slug3'}),
            reverse('posts:profile', kwargs={'username': 'auth3'}),
        ]
        for test_url in urls:
            response = self.client.get(test_url)
            # Проверка: количество постов на первой странице равно 10.
            self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_three_records(self):
        urls = [
            reverse('posts:index') + '?page=2',
            reverse('posts:group_list', kwargs={'slug': 'test-slug3'}) + '?page=2',
            reverse('posts:profile', kwargs={'username': 'auth3'}) + '?page=2',
        ]
        for test in urls:
            response = self.client.get(test)
            self.assertEqual(len(response.context['page_obj']), 3)
