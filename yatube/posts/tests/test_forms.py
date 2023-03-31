import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Post, Group, Comment


User = get_user_model()

# Создаем временную папку для медиа-файлов;
# на момент теста медиа папка будет переопределена
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


# Для сохранения media-файлов в тестах будет использоватьсяgs
# временная папка TEMP_MEDIA_ROOT, а потом мы ее удалим
@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
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

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

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
        author_1 = self.user
        group_1 = self.group
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(post_1.text, 'Текст формы')
        self.assertEqual(author_1.username, 'auth4')
        self.assertEqual(group_1.title, 'Тестовая группа4')
        self.assertRedirects(response, reverse('posts:profile', kwargs={'username': 'auth4'}))

    def test_edit_post(self):
        """Валидная форма изменяет запись в Post."""
        group_2 = Group.objects.create(
                title='Тестовая группа для формы',
                slug='test-slug-form',
                description='Тестовое описание'
        )
        post_2 = Post.objects.create(
            author=self.user,
            text='Тестовый пост',
            group=self.group
        )
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Измененный текст формы',
            'group': group_2.id,
        }
        response_edit = self.authorized_client.post(
            reverse('posts:post_edit',
                    kwargs={
                        'post_id': post_2.id
                    }),
            data=form_data,
            follow=True,
        )
        post_2 = Post.objects.get(id=post_2.id)
        self.assertEqual(response_edit.status_code, 200)
        self.assertEqual(post_2.author.username, self.user.username)
        self.assertNotEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(post_2.group.title, 'Тестовая группа для формы')
        self.assertEqual(post_2.text, 'Измененный текст формы')

    def test_guest_create_post(self):
        """Неавторизованный пользователь не может отправлять посты"""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст формы от неавторизованного пользователя',
            'group': self.group.id
        }
        response = self.guest_client.get('/create/', follow=True)
        self.guest_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertFalse(Post.objects.filter(
            text='Текст формы от неавторизованного пользователя').exists())
        self.assertRedirects(response, '/auth/login/?next=/create/')
        self.assertNotEqual(Post.objects.count(), posts_count + 1)

    def test_create_post_with_image(self):
        """Валидная форма создает запись в Post."""
        posts_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )

        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )

        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id,
            'image': uploaded,
        }

        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )

        self.assertRedirects(response, reverse('posts:profile', kwargs={'username': 'auth4'}))
        self.assertEqual(Post.objects.count(), posts_count+1)
        self.assertTrue(Post.objects.filter(
            text='Тестовый текст',
            group=self.group.id,
            image='posts/small.gif',
            ).exists()
        )

    def test_comment_post_guest_user(self):
        """Неавторизованный пользователь не может комментировать посты"""
        post = Post.objects.create(
            author=self.user,
            text='Тестовый пост',
            group=self.group,
        )
        comment_count = Comment.objects.count()
        form_data = {
            'text': 'Текст комментария от неавторизованного пользователя',
        }
        response = self.guest_client.get(f'/posts/{post.id}/comment/', follow=True)
        self.guest_client.post(
            reverse('posts:add_comment', kwargs={'post_id': post.id}),
            data=form_data,
            follow=True,
        )
        self.assertFalse(Comment.objects.filter(
            text=form_data['text']).exists())
        self.assertRedirects(response, f'/auth/login/?next=/posts/{post.id}/comment/')
        self.assertNotEqual(Comment.objects.count(), comment_count + 1)
