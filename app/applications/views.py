from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
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