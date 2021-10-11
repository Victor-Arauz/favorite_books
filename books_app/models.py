from django.contrib.messages.api import error
from django.db import models
import re
import bcrypt
from django.shortcuts import redirect


class BookManager(models.Manager):
    def bookValidator(self, formData):
        errors = {}

        if len(formData['title']) < 2:
            errors['titleLength'] = 'Title must be at least 2 characters long!'

        if len(formData['desc']) < 3 or len(formData['desc']) > 600:
            errors['descLength'] = 'Description must be between 3 and 600 characters!'
         

        return errors

class UserManager(models.Manager):

    def loginValidator(self, formData):

        errors = {}
        matchingEmail = User.objects.filter(email = formData['email'])

        if len(formData['email']) < 1:
            errors['emailRequired'] = 'Email field must be filled out!'

        elif len(matchingEmail) == 0:
            errors['emailNotfound'] = 'Email is not registered. Please register first!'
        
        if len(formData['password']) < 8:
            errors['passwordRequired'] = 'Password must be at least 8 characters long!'

        elif not bcrypt.checkpw(formData['password'].encode(), matchingEmail[0].password.encode()):
            errors['passwordWrong'] = 'Password is incorrect!'
    
        return errors

    def registrationValidator(self, formData):

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}

        matchingEmail = User.objects.filter(email = formData['email'])

        if len(formData['first_name']) < 2:
            errors['first_nameRequired'] = "First Name should be at least 2 characters long!"

        if len(formData['last_name']) < 2:
            errors['last_nameRequired'] = 'Last Name should be at least 2 characters long!'

        if len(formData['email']) < 1:
            errors['emailRequired'] = 'Email field must be filled out!'

        elif not EMAIL_REGEX.match(formData['email']):    # test whether a field matches the pattern            
            errors['emailInvalid'] = "Invalid email address!"

        elif len(matchingEmail) > 0:
            errors['emailTaken'] = "This email is already taken!"
            
        
        if len(formData['password']) < 8:
            errors['passwordRequired'] = 'Password must be at least 8 characters long!'

        if formData['password'] != formData['confirm_password']:
            errors['passwordMatch'] = 'Passwords must match!'


        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length= 60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    #liked_books = a list of books a given user likes
    #books_uploaded = a list of books uploaded by a given user

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name= 'books_uploaded', on_delete = models.CASCADE)
        # the user who uploaded a given book
    users_who_like = models.ManyToManyField(User, related_name='liked_books')
        # a list of users who like a given book
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
    def __str__(self):
        return f"{self.title} {self.id}"