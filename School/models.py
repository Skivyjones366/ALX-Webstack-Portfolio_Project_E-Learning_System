from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    cat_name = models.CharField(max_length=100)

    def __str__(self):
        return self.cat_name


class Course(models.Model):
    """ class course to """
    title = models.CharField(max_length=200, blank=False, null=False, unique=True)
    description = RichTextUploadingField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    duration = models.CharField(max_length=100, blank=True, null=True)
    cover = models.ImageField(upload_to='media')
    detail = RichTextUploadingField(blank=True, null=True)
    intro = models.FileField(upload_to='media', blank=True)
    # certificate = models.FileField(upload_to='media', blank=True, null=True)

    """def __str__(self):
        return self.id"""


class Reference(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='media')
    description = models.CharField(max_length=300, blank=True, null=True)


class Module(models.Model):
    """ class module """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)

    """def __str__(self):
        return "{} - {}".format(self.course.title, self.title)"""


class Content(models.Model):
    """ content of the course """
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=False, null=True)
    file = models.FileField(upload_to='media', blank=False)


ROLE_CHOICES = {
    ('Student', 'Student'),
    ('Teacher', 'Teacher'),
    ('Staff', 'Staff'),
}


class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True, choices=ROLE_CHOICES)
    profile_picture = models.ImageField(upload_to='media', blank=True, null=True)


class TakenCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
