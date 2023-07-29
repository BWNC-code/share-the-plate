from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from share_the_plate.models import *
from unittest.mock import patch


class TestViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.username = "testuser"
        cls.password = "12345"
        cls.user = User.objects.create_user(
            cls.username, "testemail@test.com", cls.password
        )

        cls.category = Category.objects.create(name="Test Category")

        cls.recipe = Recipe.objects.create(
            title="Test Recipe",
            slug="test-recipe",
            ingredients="Test Ingredients",
            instructions="Test Instructions",
            cooking_time=30,
            difficulty_level="beginner",
            user=cls.user,
            status=1,
        )

        cls.recipe.categories.add(cls.category)
        cls.recipe.save()

    def setUp(self):
        # Set up data for each test
        self.client = Client()
        self.client.login(username=self.username, password=self.password)

    def test_profile_info(self):
        response = self.client.get(
            reverse(
                "share_the_plate:profile_info",
                kwargs={"username": self.username}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "share_the_plate/profile_info.html")
        self.assertEqual(
            response.context["user"].username, self.username
        )  # Check if the correct user is retrieved

    def test_user_recipes(self):
        response = self.client.get(
            reverse(
                "share_the_plate:user_recipes",
                kwargs={"username": self.username}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "share_the_plate/user_recipes.html")
        self.assertEqual(
            len(response.context["recipes"]), 1
        )  # Check if the correct number of recipes is retrieved
        self.assertEqual(
            response.context["recipes"][0].title, "Test Recipe"
        )  # Check if the correct recipe is retrieved

    def test_liked_recipes(self):
        Like.objects.create(user=self.user, recipe=self.recipe)
        response = self.client.get(
            reverse(
                "share_the_plate:liked_recipes",
                kwargs={"username": self.username}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "share_the_plate/liked_recipes.html")
        self.assertEqual(
            len(response.context["liked_recipes"]), 1
        )  # Check if the correct number of liked recipes is retrieved
        self.assertEqual(
            response.context["liked_recipes"][0].title, "Test Recipe"
        )  # Check if the correct liked recipe is retrieved

    def test_signup(self):
        response = self.client.get(reverse("share_the_plate:signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "share_the_plate/sign_up.html")

    def test_after_logout(self):
        self.client.logout()  # Perform a logout before the test
        response = self.client.get(reverse("share_the_plate:after_logout"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "share_the_plate/after_logout.html")

    def test_deactivate_account(self):
        response = self.client.get(
            reverse(
                "share_the_plate:deactivate_confirm",
                kwargs={"username": self.username}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "share_the_plate/deactivate_confirm.html"
        )

    # Test POST request (should deactivate the account
    # and render the deactivated page)
        response = self.client.post(
            reverse(
                "share_the_plate:deactivated_account",
                kwargs={"username": self.username},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "share_the_plate/deactivated_user.html"
        )

    def test_toggle_like(self):
        response = self.client.post(
            reverse(
                "share_the_plate:toggle_like",
                kwargs={"slug": self.recipe.slug}
            )
        )
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_recipe_list(self):
        response = self.client.get(reverse("share_the_plate:recipe_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "share_the_plate/recipe_list.html")
        self.assertEqual(
            len(response.context["category_recipes"]), 1
        )  # Check one main recipe is retrieved

    def test_recipe_detail(self):
        response = self.client.get(
            reverse(
                "share_the_plate:recipe_detail",
                kwargs={"slug": self.recipe.slug}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "share_the_plate/recipe_detail.html")
        self.assertEqual(
            response.context["recipe"].title, "Test Recipe"
        )  # Check if the correct recipe is retrieved

    def test_search(self):
        response = self.client.get(
            reverse("share_the_plate:search"), {"q": "Test Recipe"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "share_the_plate/search_results.html"
            )
        self.assertEqual(
            len(response.context["results"]), 1
        )  # Check if the correct number of search results is retrieved
        self.assertEqual(
            response.context["results"][0].title, "Test Recipe"
        )  # Check if the correct search result is retrieved

    def test_profile_info_invalid_user(self):
        response = self.client.get(
            reverse(
                "share_the_plate:profile_info",
                kwargs={"username": "invalid_user"}
            )
        )
        # Assuming you redirect to a 404 page for invalid users
        self.assertEqual(response.status_code, 404)

    def test_user_recipes(self):
        response = self.client.get(
            reverse(
                "share_the_plate:user_recipes",
                kwargs={"username": self.username}
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "share_the_plate/user_recipes.html")
        self.assertEqual(
            len(response.context["user_recipes"]), 1
        )  # Check if the correct number of recipes is retrieved

    def test_liked_recipes_invalid_user(self):
        response = self.client.get(
            reverse(
                "share_the_plate:liked_recipes",
                kwargs={"username": "invalid_user"}
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_deactivate_account_invalid_user(self):
        response = self.client.get(
            reverse(
                "share_the_plate:deactivate_confirm",
                kwargs={"username": "invalid_user"},
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_toggle_like_invalid_recipe(self):
        response = self.client.post(
            reverse(
                "share_the_plate:toggle_like",
                kwargs={"slug": "invalid-recipe"}
            )
        )
        # Assuming you return a 404 status for invalid recipes
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_invalid_recipe(self):
        response = self.client.get(
            reverse(
                "share_the_plate:recipe_detail",
                kwargs={"slug": "invalid-recipe"}
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_search_invalid_query(self):
        response = self.client.get(
            reverse("share_the_plate:search"), {"q": "Invalid Recipe"}
        )
        self.assertEqual(response.status_code, 200)
    # Assuming the search results page is still returned, but with no results
        self.assertEqual(len(response.context["results"]), 0)
