from django.forms import ModelForm
from .models import Profile
class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		fields = ['name', 'last_name', 'email', 'birthday']