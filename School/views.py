from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from . models import *
from . forms import *


def home(request):
    """ method home to render data to homepage """
    title = "Home Page"
    courses = Course.objects.all()

    if request.method == 'POST':
        q = request.POST.get('search-q')
        mul_q = Q(Q(id__icontains=q) | Q(title__icontains=q) | Q(category__cat_name__icontains=q)
                  | Q(duration__icontains=q))
        courses = Course.objects.filter(mul_q)

    context = {
        'title': title,
        'courses': courses,
    }
    return render(request, "home.html", context)


def all_courses(request):
    """ to list all courses """
    title = "Courses"
    courses = Course.objects.all()
    category = Category.objects.all()

    if request.method == 'POST':
        values = request.POST.get('keyword')
        values = values.split(',')
        values = values[:-1]
        q = request.POST.get('search-q')
        mul_q = Q(Q(id__icontains=q) | Q(title__icontains=q) | Q(category__cat_name__icontains=q)
                  | Q(duration__icontains=q))
        if values:
            courses = Course.objects.filter(category__in=Category.objects.filter(id__in=values)).filter(mul_q)
        else:
            courses = Course.objects.filter(mul_q)

    context = {
        'courses': courses,
        'category': category,
        'title': title,
    }
    return render(request, "allCourse.html", context)


def course_detail(request, pk):
    """ to render course detail and enrol the user """
    title = "Course Detail"
    course = Course.objects.filter(id=pk)
    reference = Reference.objects.filter(course_id=pk)
    module = Module.objects.filter(course_id=pk)
    content = Content.objects.all()

    """ to collect user data when enrol """
    current_user = request.user
    form = TakenCourseForm(request.POST, None)
    if request.method == "POST":
        if current_user.is_authenticated:
            if not TakenCourse.objects.filter(user_id=current_user, course_id=pk):
                """ to check if the user already enrol this course
                if not role it, this will add the course to user """
                taken_course = TakenCourse()
                taken_course.user_id = current_user.id
                taken_course.course_id = pk
                taken_course.save()
                return redirect('/course/{}/'.format(pk))
            else:
                """ if already enrolled it will redirect to the course """
                return redirect('/course/{}/'.format(pk))
        else:
            print("Not a")
            return redirect('/')

    context = {
        'course': course,
        'module': module,
        'content': content,
        'form': form,
        'reference': reference,
        'title': title,
    }
    return render(request, "courseDetail.html", context)


@login_required
def course(request, pk):
    """ this open the course and make it ready for user """
    course = Course.objects.filter(id=pk)
    reference = Reference.objects.filter(course_id=pk)
    module = Module.objects.filter(course_id=pk)
    content = Content.objects.all()
    form = ModuleForm(request.POST)
    title = course

    context = {
        'course': course,
        'module': module,
        'content': content,
        'form': form,
        'reference': reference,
        'title': title,
    }
    return render(request, "course.html", context)


@staff_member_required
def add_course(request):
    """ To add a course """
    title = "Add Course"
    form = CourseForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Course successfully added")
            return redirect('/allCourses')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect(url)

    context = {
        'form': form,
        'title': title,
    }
    return render(request, "add_course.html", context)


@staff_member_required
def edit_course(request, pk):
    """ To edit the course """
    title = "Edit Course"
    course = Course.objects.get(id=pk)
    form = CourseForm(instance=course)
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course '{}' successfully edited".format(course.title))
            return redirect('/course/{}/'.format(pk))

    context = {
        'form': form,
        'title': title,
    }
    return render(request, "add_course.html", context)


@staff_member_required
def add_reference(request):
    """ to add content """
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = ReferenceForm(request.POST, request.FILES)
        if form.is_valid():
            reference = Reference()
            reference.course = form.cleaned_data['course']
            reference.name = form.cleaned_data['name']
            reference.file = form.cleaned_data['file']
            reference.description = form.cleaned_data['description']
            reference.save()
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect(url)
        return redirect(url)


@staff_member_required
def add_module(request):
    """ to add module """
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = ModuleForm(request.POST, None)
        if form.is_valid():
            module = Module()
            module.course = form.cleaned_data['course']
            module.title = form.cleaned_data['title']
            module.duration = form.cleaned_data['duration']
            module.save()
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect(url)
        return redirect(url)


@staff_member_required
def add_content(request):
    """ to add content """
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            content = Content()
            content.module = form.cleaned_data['module']
            content.name = form.cleaned_data['name']
            content.file = form.cleaned_data['file']
            content.save()
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect(url)
        return redirect(url)


@login_required
def my_courses(request):
    """ to render list of course depending on user """
    title = "My Courses"
    usr = request.user
    my_course = TakenCourse.objects.filter(user_id=usr.id)
    context = {
        'title': title,
        'my_course': my_course,
    }
    return render(request, 'my_courses.html', context)


@login_required
def my_account(request, pk):
    """ to render account detail """
    title = "My Account"
    my = UserDetail.objects.filter(user_id=pk)
    context = {
        'title': title,
        'my': my,
    }
    return render(request, 'my_account.html', context)


def contact(request):
    """ to render contact page """
    title = "Contact"
    context = {
        'title': title,
    }
    return render(request, 'contact.html', context)


def about(request):
    """ to render contact page """
    title = "About"
    context = {
        'title': title,
    }
    return render(request, 'about.html', context)
