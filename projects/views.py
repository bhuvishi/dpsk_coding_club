from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . models import Project
from .forms import ProjectForm
from users.forms import UpdateUserInfoForm, UserImageExtensionForm
from django.core.paginator import Paginator

@login_required()
def home_page(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        form.instance.posted_by = request.user
        if form.is_valid():
            form.save()
            return redirect('project-home')
    else:
        form = ProjectForm()

    number_of_personal_projects = len(Project.objects.filter(posted_by=request.user.id))
    all_projects = Project.objects.order_by('-post_date')
    paginator = Paginator(all_projects, 3)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'projects': page,
        'number_of_personal_projects': number_of_personal_projects,
        'form': form
    }
    return render(request, 'projects/home.html', context)

@login_required()
def single_project(request, project_id, update=None):
    project = Project.objects.get(id=project_id)
    update_screen = True if update == 'update' else False
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project.title = form.instance.title
            project.body = form.instance.body
            project.save()
            return redirect('project-home')
    else:
        form = ProjectForm(initial={'title': project.title, 'body': project.body})
    context = {
        'project': project,
        'form': form,
        'update': update_screen,
    }
    return render(request, 'projects/single_project.html', context)

@login_required()
def delete_project(request, project_id):
    Project.objects.filter(id=project_id).delete()
    return redirect('post-home')

@login_required()
def account_page(request):
    if request.method == 'POST':
        user_update_info_form = UpdateUserInfoForm(request.POST, instance=request.user)
        if hasattr(request.user, 'userimageextension'):
            user_image_extension_form = UserImageExtensionForm(
                request.POST, request.FILES, instance=request.user.userimageextension)
        else:
            user_image_extension_form = UserImageExtensionForm(
                request.POST, request.FILES)
            user_image_extension_form.instance.user = request.user

        if user_update_info_form.is_valid() and user_image_extension_form.is_valid():
            user_update_info_form.save()
            user_image_extension_form.save()
            messages.success(request, 'Account Updated!')
            return redirect('project-account')
    else:
        user_update_info_form = UpdateUserInfoForm(instance=request.user)
        if hasattr(request.user, 'userimageextension'):
            user_image_extension_form = UserImageExtensionForm(instance=request.user.userimageextension)
        else:
            user_image_extension_form = UserImageExtensionForm()
    context = {
        'user_update_info_form': user_update_info_form,
        'user_image_extension_form': user_image_extension_form
    }
    return render(request, 'projects/account.html', context)

@login_required()
def about_page(request):
    return render(request, 'projects/about.html')