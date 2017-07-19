import json
import os
import requests

from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        base_link = 'http://localhost:8000/applications/applicant/'
        slack_message = '%(name)s just applied to Equipo please checkout his/her <%(link)s|application>' \
                        % {'name': 'someone', 'link': base_link + '1' + '/'}
        payload = {'text': slack_message}
        headers = {'content-type': 'application/json'}
        requests.post(os.environ.get('SLACK_WEBHOOK_URL'), data=json.dumps(payload), headers=headers)
