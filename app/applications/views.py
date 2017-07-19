import json
import os
import requests

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import mail
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from .forms import *
from .models import *

# Create your views here.


def apply(request):
    if request.method == 'POST':
        application_form = ApplicationForm(request.POST or None)

        if application_form.is_valid():
            applicant = application_form.save()

            # Send confirmation mail to the applicant.
            subject = 'Thank you for applying to Equipo!'
            message = 'Hello %(name)s we at WebMonks like to thank you for applying to Equipo.' \
                      'Your application will be viewed A.S.A.P.' % {'name': applicant.name}
            mail_from = 'noreply@webmonks.io'
            mail_to = applicant.email

            send_mail(
                subject,
                message,
                mail_from,
                [mail_to],
            )

            # Send notification to the WebMonks Slack channel
            base_link = 'http://localhost:8000/applications/applicant/'
            slack_message = '%(name)s just applied to Equipo please checkout his/her <%(link)s|application>' \
                            % {'name': applicant.name, 'link': base_link + str(applicant.pk) + '/'}
            payload = {'text': slack_message}
            headers = {'content-type': 'application/json'}
            requests.post(os.environ.get('SLACK_WEBHOOK_URL'), data=json.dumps(payload), headers=headers)

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
