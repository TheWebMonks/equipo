from django.forms import ModelForm
from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from django.utils.safestring import mark_safe
from string import Template
import  django.template.loader
from . import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, HTML
from crispy_forms.bootstrap import StrictButton, FieldWithButtons
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions)


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password (Again)', widget=forms.PasswordInput())

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
            raise forms.ValidationError('Username is already taken.')

        raise forms.ValidationError('Passwords do not match.')


class DateInput(forms.DateInput):
    input_type = 'date'


class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs={ 'width':'150', 'height':'150'}):
        html = Template("""<img src="$link"/>""")

        return mark_safe(html.substitute(link=value))


class ProfileForm(ModelForm):
    class Meta:
        model = models.Profile
        fields = ['type', 'name', 'resume', 'last_name', 'email', 'birthday', 'skills', 'personal_page', 'country',
                  'city', 'telephone', 'photo']
        widgets = {
            'birthday': DateInput(),
            'photo': PictureWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        my_field_text = [
            ('type', 'Title'),
            ('name', 'Name'),
            ('resume', 'Resume'),
            ('last_name', 'Last name'),
            ('email', 'email'),
            ('birthday', 'Birthday'),
            ('skills', 'Tech Skills'),
            ('personal_page', 'Web page'),
            ('country', 'Country'),
            ('city', 'City'),
            ('telephone', 'Telephone'),
            ('photo', 'Photo')]
        for x in my_field_text:
            self.fields[x[0]].label = x[1]
            #self.fields[x[0]].help_text = x[1]
            # Set layout for fields.
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div('name', css_class='col-xs-4'),
                Div('last_name', css_class='col-xs-4'),
                Div('birthday', css_class='col-xs-4'),
                css_class='row',
            ),
            Div(
                Div('email', css_class='col-xs-6'),
                Div('personal_page', css_class='col-xs-6'),
                css_class='row',
            ),
            Div(
                Div('country', css_class='col-xs-4'),
                Div('city', css_class='col-xs-4'),
                Div('telephone', css_class='col-xs-4'),
                css_class='row',
            ),
            Div('resume'),
            Div(
                Div('type', css_class='col-xs-6'),
                Div('skills', css_class='col-xs-6'),
                css_class='row',
            ),
            Div(
                FieldWithButtons('photo', HTML('<input type="file" name="photo" css_class="col-xs-6" '
                                               'value="Select image"> <br>'
                                                '<input type="checkbox" name="gravatar"> Use my gravatar')),
                css_class='row',
            ),
        )

        self.helper.layout.append(HTML('<input type="checkbox" name="gravatar"> Use my gravatar'
                                '<hr>'
                                '<label class="control-label">Education & Experience</label>'
                                '<ul>'
                                '<li><a id="create-experience" href="{% url "experience" %}" class="fm-create" '
                                'data-fm-head="Create" data-fm-callback="reload">Add Work Experience</a></li>'
                                '<li><a id="create-experience" href="{% url "education" %}" class="fm-create" '
                                'data-fm-head="Create" data-fm-callback="reload">Add Education</a></li>'
                                '</ul>'))
        self.helper.add_input(Submit('submit', 'Submit'))

class SkillForm(ModelForm):
    class Meta:
        model = models.Skill
        fields = ['tag', 'description']


class SocialNetworkForm(ModelForm):
    class Meta:
        model = models.SocialNetwork
        fields = ['name']


class SocialAccount(ModelForm):
    class Meta:
        model = models.SocialAccount
        fields = ['web_address','user', 'name']


class ExperienceForm(ModelForm):
    class Meta:
        model = models.Experience
        fields = ['role', 'description', 'date']
        widgets = {
            'date': DateInput(),
        }


class EducationForm(ModelForm):
    class Meta:
        model = models.Education
        fields = ['university', 'degree', 'date']
        widgets = {
            'date': DateInput(),
        }


class TypeOfContractForm(ModelForm):
    class Meta:
        model = models.TypeOfContract
        fields = ['name', 'description']


class ProfileSkillForm(ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=models.Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = models.Skill
        fields = ['tag', 'description']


class ProjectContractForm(ModelForm):
    type_of_contract = forms.ModelMultipleChoiceField(
        queryset=models.TypeOfContract.objects.all(),
        widget=forms.Select)

    class Meta:
        model = models.TypeOfContract
        fields = ['name', 'description']


class ProjectForm(ModelForm):
    class Meta:
        model = models.Project
        fields = ['description', 'required_skills']


class CompanyForm(ModelForm):
    class Meta:
        model = models.Company
        fields = ['name', 'email', 'web_page', 'description', 'logo']
        widgets = {
            'logo': PictureWidget(),
        }


class CategoryForm(ModelForm):
    class Meta:
        model = models.Category
        fields = ['name', 'description']


class KindOfTaskForm(ModelForm):
    class Meta:
        model = models.KindOfTask
        fields = ['name','description']


class ExpenseForm(ModelForm):
    class Meta:
        model = models.Expense
        fields = ['project', 'category','notes', 'amount', 'date']


class InvoiceForm(ModelForm):
    class Meta:
        model = models.Invoice
        fields = ['project','start_time', 'stop_time']


class ContractForm(ModelForm):
    class Meta:
        model = models.Contract
        fields = ['project']


class ExpendedTimeForm(ModelForm):
    class Meta:
        model = models.ExpendedTime
        fields = ['project', 'kind_of_task', 'notes', 'time', 'start_time', 'stop_time']


class SearchInvoiceForm(ModelForm):
    project = forms.ChoiceField()
    start_date =  forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())
    invoices = forms.ChoiceField()

    class Meta:
        model = models.Project
        fields = ['project', 'start_date','end_date', 'invoices']
        widgets = {
            'project':forms.Select(),
            'start_date': DateInput(),
            'end_date': DateInput(),
            'invoices': forms.Select()
        }

    def __init__(self, *args, **kwargs):
        super(SearchInvoiceForm, self).__init__(*args, **kwargs)
        user_profile = kwargs.get('user_profile')

        if user_profile is None:
            projects = models.Project.objects.all()
        else:
            projects = models.Project.objects.filter(freelancers=user_profile)

        self.fields['project'].choices = projects.values_list('id', 'name')
        self.fields['invoices'].required = False
        INVOICE_CHOICES = (
            (0, ('Select an Option')),
        )
        # self.fields['invoices'].choices = INVOICE_CHOICES

