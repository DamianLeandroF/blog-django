from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AutenticacionTests(TestCase):
    def test_registro_login_logout(self):
        response = self.client.post(reverse('accounts:registro'), {
            'username': 'nuevo', 'email': 'n@example.com',
            'password1': 'ClaveSegura#2026', 'password2': 'ClaveSegura#2026',
        })
        self.assertRedirects(response, reverse('posts:list'))
        self.assertTrue(User.objects.filter(username='nuevo').exists())
        self.assertTrue(User.objects.get(username='nuevo').perfil)

        self.client.post(reverse('accounts:logout'))
        self.assertEqual(self.client.get(reverse('accounts:perfil')).status_code, 302)

        response = self.client.post(reverse('accounts:login'), {'username': 'nuevo', 'password': 'ClaveSegura#2026'})
        self.assertRedirects(response, reverse('posts:list'))
        self.assertEqual(self.client.get(reverse('accounts:perfil')).status_code, 200)

    def test_perfil_requiere_login(self):
        response = self.client.get(reverse('accounts:perfil'))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('accounts:perfil')}")
