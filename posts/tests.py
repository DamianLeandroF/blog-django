import io

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Post

User = get_user_model()


def imagen_de_prueba():
    buffer = io.BytesIO()
    Image.new('RGB', (10, 10), 'red').save(buffer, 'PNG')
    return SimpleUploadedFile('test.png', buffer.getvalue(), content_type='image/png')


class RutasProtegidasTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('ana', 'ana@example.com', 'pass12345!')
        self.post = Post.objects.create(titulo='Hola', contenido='Mundo', autor=self.user)

    def test_anonimo_es_redirigido(self):
        urls = [
            reverse('posts:create'),
            reverse('posts:update', args=[self.post.pk]),
            reverse('posts:delete', args=[self.post.pk]),
            reverse('accounts:editar_perfil'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn(reverse('accounts:login'), response.url)

    def test_anonimo_puede_ver_listado_y_detalle(self):
        self.assertEqual(self.client.get(reverse('posts:list')).status_code, 200)
        self.assertEqual(self.client.get(self.post.get_absolute_url()).status_code, 200)

    def test_otro_usuario_no_puede_editar(self):
        User.objects.create_user('beto', 'b@example.com', 'pass12345!')
        self.client.login(username='beto', password='pass12345!')
        self.assertEqual(self.client.get(reverse('posts:update', args=[self.post.pk])).status_code, 403)


class CrudTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('ana', 'ana@example.com', 'pass12345!')
        self.client.login(username='ana', password='pass12345!')

    def test_crud_completo_con_imagen(self):
        with override_settings(MEDIA_ROOT=self.enterContext(__import__('tempfile').TemporaryDirectory())):
            response = self.client.post(reverse('posts:create'), {
                'titulo': 'Nuevo', 'contenido': 'Texto', 'imagen': imagen_de_prueba(),
            })
            post = Post.objects.get()
            self.assertRedirects(response, post.get_absolute_url())
            self.assertTrue(post.imagen)
            self.assertContains(self.client.get(post.get_absolute_url()), post.imagen.url)

        self.client.post(reverse('posts:update', args=[post.pk]), {'titulo': 'Editado', 'contenido': 'Texto'})
        post.refresh_from_db()
        self.assertEqual(post.titulo, 'Editado')

        self.client.post(reverse('posts:delete', args=[post.pk]))
        self.assertFalse(Post.objects.exists())

    def test_template_sin_imagen(self):
        post = Post.objects.create(titulo='Sin imagen', contenido='x', autor=self.user)
        self.assertEqual(self.client.get(reverse('posts:list')).status_code, 200)
        self.assertEqual(self.client.get(post.get_absolute_url()).status_code, 200)


class BusquedaTests(TestCase):
    def setUp(self):
        user = User.objects.create_user('ana', 'ana@example.com', 'pass12345!')
        Post.objects.create(titulo='Django avanzado', contenido='vistas', autor=user)
        Post.objects.create(titulo='Otro', contenido='habla de Python', autor=user)

    def test_busca_por_titulo_y_contenido(self):
        self.assertEqual(len(self.client.get(reverse('posts:list'), {'q': 'django'}).context['posts']), 1)
        self.assertEqual(len(self.client.get(reverse('posts:list'), {'q': 'python'}).context['posts']), 1)

    def test_sin_coincidencias(self):
        response = self.client.get(reverse('posts:list'), {'q': 'zzz'})
        self.assertContains(response, 'No se encontraron posts')
