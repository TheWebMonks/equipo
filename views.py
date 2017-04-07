from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Profile
from django.template import loader
from django.urls import reverse
from django.views import generic
from .forms import ProfileForm
# Create your views here.

class IndexView(generic.ListView):
	template_name = 'freelancers/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""Return the last five published questions."""
		return Profile.objects.order_by('id')
def add_profile(request):
		if request.method == 'POST':
			form = ProfileForm(request.POST)

			if form.is_valid():
				new_profile = form.save();
				return HttpResponse("<h3>Thanks<h3> <li><a href='/Freelancers'>Return to index</a></li>")

		else:
			form = ProfileForm()
		
		return render(request,'freelancers/add.html',{'form': form})

def update_profile(request,pk):
		if request.method == 'POST':
			instance = get_object_or_404(Profile, pk=pk)
			form = ProfileForm(request.POST or None, instance=instance)
			if form.is_valid():
				form.save();
				return HttpResponse("<h3>Thanks<h3> <li><a href='/Freelancers'>Return to index</a></li>")
		else:
			a = Profile.objects.get(pk=pk)
			form = ProfileForm(instance=a)
		
		return render(request,'freelancers/update.html',{'form': form, 'id' : pk})

class ResultsView(generic.DetailView):
	model = Profile
	template_name = 'freelancers/results.html'

def vote(request, pk):
    return HttpResponse("You're voting on question %s." % pk)