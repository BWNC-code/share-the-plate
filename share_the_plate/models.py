from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from cloudinary.models import CloudinaryField
from taggit.managers import TaggableManager

# Create your models here.

STATUS = ((0, "Draft"), (1, "Published"))

DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = CloudinaryField('image', default='https://res.cloudinary.com/share-the-plate-cloud/image/upload/v1690650210/static/assets/images/default_profile.eba7a5674add.jpg')


class Recipe(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    ingredients = models.TextField()
    instructions = models.TextField()
    cooking_time = models.IntegerField(
        help_text='Enter cooking time in minutes'
    )
    difficulty_level = models.CharField(
        max_length=15,
        choices=DIFFICULTY_CHOICES,
        default='beginner',
    )
    featured_image = CloudinaryField('image', default='https://res.cloudinary.com/share-the-plate-cloud/image/upload/v1690654327/static/assets/images/placeholder_image.b16bf0e41648.jpg')
    categories = models.ManyToManyField('Category', related_name='recipes')
    tags = TaggableManager(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'share_the_plate:recipe_detail',
            kwargs={'slug': self.slug}
        )


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment {self.body} by {self.user.username}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')
