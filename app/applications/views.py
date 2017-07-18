from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from .models import *

# Create your views here.


def apply(request):
    if request.method == 'POST':
        application_form = ApplicationForm(request.POST or None)

        if application_form.is_valid():
            application_form.save()
            messages.success(request, 'Form submission successful')
        else:
            messages.error(request, 'Form submission Error')

    else:
        application_form = ApplicationForm()

    return render(request, 'applications/application.html', {'form': application_form})

@login_required
def get_all(request):
    applicants_all = Applicant.objects.all()
    return render(request, 'applications/applicants.html', {'applicants': applicants_all})


@login_required
def applicant(request, pk):
    applicant = Applicant.objects.get(pk=pk)
    application_form = ApplicationForm(instance=applicant)

    return render(request, 'applications/applicant.html', {'applicant': applicant, 'application_form': application_form})

@login_required
def create_comment(request, pk):
    applicant = Applicant.objects.get(pk=pk)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.applicant = applicant
            comment.admin = request.user
            comment.save()
            messages.success(request, 'Form submission successful')
            return redirect('applications:applicant', pk=pk)

        else:
            messages.error(request, 'Form submission Error ')

    else:
        comment_form = CommentForm()

    return render(request, 'applications/comment.html', {'applicant': applicant, 'comment_form': comment_form})
