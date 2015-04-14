from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
	# return HttpResponse("hello")
	return render(request, 'index.html', {})

def search(request):
	return HttpResponseRedirect(reverse('app:search_results', args=()))

def search_results(request):
	summary = [1,5,3,4,5,6]
		# return render(request, 'tldr/summary.html', { 'summary': summary })
	return render(request, 'search_results.html', {'summary':summary})
