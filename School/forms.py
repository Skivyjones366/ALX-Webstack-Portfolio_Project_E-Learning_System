from django import forms
from .models import *


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'category', 'duration', 'cover', 'intro', 'detail', 'description']


class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = '__all__'


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = '__all__'


class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = '__all__'


class UserDetailForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = '__all__'


class TakenCourseForm(forms.ModelForm):
    class Meta:
        model = TakenCourse
        fields = '__all__'


class UserDetailForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = '__all__'
