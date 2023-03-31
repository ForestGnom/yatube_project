from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
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
            pk=5,
            author=cls.user,
            text='Тестовый пост',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем общедоступные страницы
    def test_homepage(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group(self):
        """Страница /group/ доступна любому пользователю."""
        response = self.guest_client.get(f'/group/{self.group.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        """Страница /profile/auth/ доступна любому пользователю."""
        response = self.guest_client.get(f'/profile/{self.user.username}/')
        self.assertEqual(response.status_code, 200)

    def test_posts_id(self):
        """Страница /posts/5/ доступна любому пользователю."""
        response = self.guest_client.get(f'/posts/{self.post.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_unexisting_page(self):
        """Страницы /privet/ не существует."""
        response = self.guest_client.get('/privet/')
        self.assertEqual(response.status_code, 404)

    # Проверяем доступность страниц для авторизованного пользователя
    def test_create(self):
        """Страница /create/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    # Проверяем доступность страниц для автора поста
    def test_posts_id_edit(self):
        """Страница /posts/5/edit/ доступна автору поста с id = 5."""
        response = self.authorized_client.get(f'/posts/{self.post.pk}/edit/')
        self.assertEqual(response.status_code, 200)

    # Проверяем редиректы для неавторизованного пользователя
    def test_create_redirect(self):
        """Страница /create/ перенаправит анонимного пользователя на страницу логина."""
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(response, f'/{self.user.username}/login/?next=/create/')

    def test_posts_id_edit_redirect(self):
        """Страница /posts/5/edit/ перенаправит анонимного пользователя на страницу логина."""
        response = self.guest_client.get(f'/posts/{self.post.pk}/edit/')
        self.assertRedirects(response, f'/auth/login/?next=/posts/{self.post.pk}/edit/')

    # Проверка вызываемых шаблонов для каждого адреса
    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user.username}/': 'posts/profile.html',
            f'/posts/{self.post.pk}/': 'posts/post_detail.html',
            f'/posts/{self.post.pk}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }

        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

