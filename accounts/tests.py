from django.test import TestCase


class AccountTests(TestCase):
    def test_login_page_includes_hidden_culture_easter_egg(self):
        response = self.client.get('/giris/')

        self.assertContains(response, 'id="culture-egg"')
        self.assertContains(response, 'Hava Nagila')
        self.assertContains(response, 'hidden')

    def test_user_can_register(self):
        response = self.client.post('/kayit/', {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'StrongPass!123',
            'password2': 'StrongPass!123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.session.get('_auth_user_id'))

    def test_profile_requires_login(self):
        response = self.client.get('/profil/')
        self.assertEqual(response.status_code, 302)

    def test_user_can_login(self):
        from django.contrib.auth import get_user_model

        user = get_user_model().objects.create_user(username='loginuser', email='login@example.com', password='StrongPass!123')
        response = self.client.post('/giris/', {'username': 'loginuser', 'password': 'StrongPass!123'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
