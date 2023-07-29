# Testing Guide for Share The Plate Django Application

## Introduction

This document aims to provide a guide to how the share_the_plate Django application has been tested.

## Current Test Cases

Currently, the following automated unit test cases have been implemented:

### User Profile Information

This tests the GET request response for the profile info page of the test user. The test checks if the correct template is used and if the retrieved user information is correct.

### User's Submitted Recipes

This tests the GET request response for the user's recipes page of the test user. It validates if the correct template is used, and if the correct number and data of recipes are retrieved.

### User's Liked Recipes

This tests the GET request response for the liked recipes page of the test user. It validates if the correct template is used, and if the correct number and data of liked recipes are retrieved.

### User Sign Up

This tests the GET request response for the signup page, verifying if the correct template is used.

### After User Logout

This tests the GET request response for the after logout page, validating if the correct template is used.

### Account Deactivation

This tests both the GET and POST request responses for the account deactivation page for the test user. It checks if the correct templates are used. The POST request is expected to deactivate the account and render the deactivated page.

### Recipe Like Toggle

This tests the POST request response to toggle the like status of a recipe for the test user. It checks for the correct status code for the redirect response.

### Recipe List

This tests the GET request response for the recipe list page. It validates if the correct template is used and if the correct number of recipes are retrieved.

### Recipe Detail

This tests the GET request response for a recipe detail page of a test recipe. It checks if the correct template is used and if the correct recipe data is retrieved.

### Search Function

This tests the GET request response for the search function using a test query. It validates if the correct template is used, and if the correct number and data of search results are retrieved.

### Invalid User Handlers

Tests are included for handling invalid users in profile info, liked recipes, and account deactivation scenarios. These tests confirm if a 404 status code is returned for invalid users.

### Invalid Recipe Handlers

Tests are included for handling invalid recipes in the recipe like toggle and recipe detail scenarios. These tests confirm if a 404 status code is returned for invalid recipes.

### Invalid Search Query

This test handles an invalid search query scenario. It confirms if the search results page is still returned with no results for invalid queries.

All these tests are written in the tests.py file inside the share_the_plate application. You can run these tests using the Django test runner with the command python manage.py test share_the_plate.

To run a single test case or test method, you can use the Django test runner with the specific test case or test method, like python manage.py test share_the_plate.tests.TestViews.test_profile_info

## Manual Testing

Manual testing was also performed successfully for the following components:

### Registration, Login, and User Profile

1. Registered a new account through the UI and verified the account was created successfully.

2. Logged in with a valid username and password.

3. Attempted to log in with an invalid username and password and received appropriate error messages.

4. Navigated to the user profile and verified all details were displayed correctly.

5. Updated profile details and verified changes were saved and displayed correctly.

### Recipe Interaction

1. Browsed the list of recipes and verified all information was displayed correctly for each recipe.

2. Clicked on a recipe to view details and verified all information, including comments and likes, was displayed correctly.

3. Submitted a new recipe using the 'Add Recipe' form and verified the recipe was added correctly.

4. Edited an existing recipe and verified changes were saved and displayed correctly.

5. Deleted a recipe and verified it was removed from the list of recipes and the main recipe list.

6. Liked and unliked a recipe and verified the like count changed appropriately.

### Search Function Manual

1. Used the search function to look for a specific recipe and verified that the correct results were displayed.

2. Searched for a non-existent recipe and verified that appropriate messages were shown.

### Comment Interaction

1. Added a comment to a recipe and verified it was displayed correctly.

2. Edited a comment and verified changes were saved and displayed correctly.

3. Deleted a comment and verified it was removed from the list of comments.

### Account Deactivation Manual

1. Deactivated an account and verified the user was logged out and the account no longer existed.

All manual tests performed successfully, confirming the application works correctly from a user's perspective.
