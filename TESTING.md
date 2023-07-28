# Testing Guide for Share The Plate Django Application

## Introduction

This document aims to provide a guide to comprehensively test the share_the_plate Django application.

## Current Test Cases

Currently, the following automated unit test cases have been implemented:

### Profile Information Page

Tests the response of the GET request to the profile info page for the test user. The correct template was confirmed to be used.

### User's Recipes Page

Tests the response of the GET request to the user's recipes page for the test user. The correct template was confirmed to be used.

### Liked Recipes Page

Tests the response of the GET request to the liked recipes page for the test user. The correct template was confirmed to be used.

### Sign Up Page

Tests the response of the GET request to the signup page. The correct template was confirmed to be used.

### After Logout Page

Tests the response of the GET request to the after logout page. The correct template was confirmed to be used.

### Account Deactivation

Tests the response of both the GET and POST requests to the account deactivation page for the test user. It also checks if the correct templates are being used.

### Toggle Like

Tests the response of the POST request to toggle the like status of a recipe for the test user.

### Recipe List Page

Tests the response of the GET request to the recipe list page. It also checks if the correct template is being used.

### Recipe Detail Page

Tests the response of the GET request to the recipe detail page for a test recipe. It also checks if the correct template is being used.

### Search Function

Tests the response of the GET request to the search function using a test query. It also checks if the correct template is being used.