from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from share_the_plate.models import *
from unittest.mock import patch


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        # This method is for setup that is to be done at the class level and doesn't change in between different test methods
        cls.username = 'testuser'
        cls.password = '12345'
        cls.user = User.objects.create_user(cls.username, 'testemail@test.com', cls.password)

        cls.category = Category.objects.create(
            name='Test Category'
        )

        cls.recipe = Recipe.objects.create(
            title='Test Recipe',
            slug='test-recipe',
            ingredients='Test Ingredients',
            instructions='Test Instructions',
            cooking_time=30, 
            difficulty_level='beginner', 
            user=cls.user,
            status=1
        )

        # add the test category to the recipe
        cls.recipe.categories.add(cls.category)

        # save the recipe instance
        cls.recipe.save()

    def setUp(self):
        # This method is for setup that could be changed by the tests themselves, and will run before each test
        self.client = Client()
        self.client.login(username=self.username, password=self.password)

    def test_profile_info(self):
        response = self.client.get(reverse('share_the_plate:profile_info', kwargs={'username': self.username}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'share_the_plate/profile_info.html')

    def test_user_recipes(self):
        response = self.client.get(reverse('share_the_plate:user_recipes', kwargs={'username': self.username}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'share_the_plate/user_recipes.html')

    def test_liked_recipes(self):
        Like.objects.create(user=self.user, recipe=self.recipe)
        response = self.client.get(reverse('share_the_plate:liked_recipes', kwargs={'username': self.username}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'share_the_plate/liked_recipes.html')

    def test_signup(self):
        response = self.client.get(reverse('share_the_plate:signup'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'share_the_plate/sign_up.html')

    def test_after_logout(self):
        response = self.client.get(reverse('share_the_plate:after_logout'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'share_the_plate/after_logout.html')

    def test_deactivate_account(self):
        # Test GET request (should render the confirmation page)
        response = self.client.get(reverse('share_the_plate:deactivate_confirm', kwargs={'username': self.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'share_the_plate/deactivate_confirm.html')

        # Test POST request (should deactivate the account and render the deactivated page)
        response = self.client.post(reverse('share_the_plate:deactivated_account', kwargs={'username': self.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'share_the_plate/deactivated_user.html')

    def test_toggle_like(self):
        response = self.client.post(reverse('share_the_plate:toggle_like', kwargs={'slug': self.recipe.slug}))

        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_recipe_list(self):
        response = self.client.get(reverse('share_the_plate:recipe_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'share_the_plate/recipe_list.html')

    def test_recipe_detail(self):
        response = self.client.get(reverse('share_the_plate:recipe_detail', kwargs={'slug': self.recipe.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'share_the_plate/recipe_detail.html')

    def test_search(self):
        response = self.client.get(reverse('share_the_plate:search'), {'q': 'Test Recipe'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'share_the_plate/search_results.html')
