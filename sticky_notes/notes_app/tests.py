from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task
from datetime import datetime


# # Create your tests here.
class TestUserAuthentication(TestCase):

    def setUp(self):
        # Create a user to test login
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')

    def test_login_with_correct_credentials(self):
        response = self.client.post(reverse('login'),
                                    {'username': 'testuser',
                                     'password': 'testpassword'})
        self.assertRedirects(response, reverse('home'))

    def test_login_with_incorrect_password(self):
        response = self.client.post(reverse('login'),
                                    {'username': 'testuser',
                                     'password': 'incorrectpassword'})
        self.assertContains(response, 'Incorrect password. Please try again.')

    def test_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))


class TestUserRegistration(TestCase):
    def test_register_new_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertRedirects(response, reverse('home'))
        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user)


class TestHomePageAccess(TestCase):
    # Create test user
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')

    def test_home_page_redirects_if_not_logged_in(self):
        # Test access to home page without logging in
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('login') + '?next='
                             + reverse('home'))

    def test_home_page_functional_if_logged_in(self):
        # Log in test user
        self.client.login(username='testuser', password='testpassword')
        # Test access to home page
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sticky Notes Task Manager')


class TestTaskCreation(TestCase):
    # Create test user and login to test task creation
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_create_task(self):
        # Prepare test task data
        task_data = {
            'title': 'Test Task',
            'description': 'Description for the test task here',
            'owner': 'Employee or colleague name',
            'due_date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'Not Started'
        }
        response = self.client.post(reverse('create_task'), data=task_data)

        # Ensure the task was created
        task = Task.objects.get(title='Test Task')
        self.assertIsNotNone(task)
        self.assertEqual(task.description, 'Description for the test task here')
        self.assertEqual(task.owner, 'Employee or colleague name')
        self.assertEqual(task.status, 'Not Started')

        # Ensure the response redirects to the home page
        self.assertRedirects(response, reverse('home'))
