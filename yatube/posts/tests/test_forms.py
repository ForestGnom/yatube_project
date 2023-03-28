from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..forms import PostForm
from ..models import Post, Group


User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth4')

        cls.group = Group.objects.create(
            title='Тестовая группа4',
            slug='test-slug4',
            description='Тестовое описание4'
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст формы',
            'group': self.group.id
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )

        post_1 = Post.objects.get(id=self.group.id)
        author_1 = User.objects.get(username='auth4')
        group_1 = Group.objects.get(title='Тестовая группа4')
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(post_1.text, 'Текст формы')
        self.assertEqual(author_1.username, 'auth4')
        self.assertEqual(group_1.title, 'Тестовая группа4')
        self.assertRedirects(response, reverse('posts:profile', kwargs={'username': 'auth4'}))

    def test_edit_post(self):
        form_data = {
            'text': 'Текст формы',
            'group': self.group.id
        }
        self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        post_2 = Post.objects.get(id=self.group.id)
        self.client.get(f'/auth4/{post_2.id}/edit/')
        form_data = {
            'text': 'Измененный текст формы',
            'group': self.group.id
        }
        response_edit = self.authorized_client.post(
            reverse('posts:post_edit',
                    kwargs={
                        'post_id': post_2.id
                    }),
            data=form_data,
            follow=True,
        )
        post_2 = Post.objects.get(id=self.group.id)
        self.assertEqual(response_edit.status_code, 200)
        self.assertEqual(post_2.text, 'Измененный текст формы')
