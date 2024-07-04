from django.contrib import admin
from django.apps import apps
from . models import *

""" one way to get models in django admin
models = apps.get_app_config('school').get_models()
for model in models:
    admin.site.register(model)"""


class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'cover', 'category', 'duration']


class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'duration']


class ReferenceAdmin(admin.ModelAdmin):
    list_display = ['course', 'name', 'file', 'description']


class ContentAdmin(admin.ModelAdmin):
    list_display = ['name', 'module', 'file']


class TakenCourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'course']


admin.site.register(Course, CourseAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Reference, ReferenceAdmin)
admin.site.register(Category)
admin.site.register(UserDetail)
admin.site.register(TakenCourse, TakenCourseAdmin)
