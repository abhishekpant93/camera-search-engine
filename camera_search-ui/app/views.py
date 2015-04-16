from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from search import search as s

# Create your views here.
data = {}
def index(request):
	# return HttpResponse("hello")
	
	return render(request, 'index.html', {})

def search(request):
	query = {}
	data = s.load_data()
	#isHasSelfTimer = False
	#isHasImageStabilization = False
	myList = []

	for k in request.POST.keys():
		if("_check" in k):
			myList.append(k[:-6])

	for k in myList:
		

		key = k
		val = request.POST[k]
		ran = val

		if("_" in k):
			key = k.replace("_"," ")
		if("," in val):
			r = val.split(",")
			ran = []
			for v in r:
				ran.append(float(v))

		#if(key == "Has Self Timer"):
	#		isHasSelfTimer = True
#		if(key == "Has Image Stabilization"):
#			isHasImageStabilization = True

		if(key == "price" or key == "Display Resolution Maximum" or key == "Optical Zoom" or key == "Optical Sensor Resolution" or key == "Memory Storage Capacity" or key == "Screen Size" or key == "Min Focal Length" or key == "Item Weight" or key == "Has Self Timer" or key == "Has Image Stabilization"):
			query[key] = ran
	
	#if(not isHasSelfTimer):
	#	query['Has Self Timer'] = 'off'
	#if(not isHasImageStabilization):
	#	query['Has Image Stabilization'] = 'off'

	results = s.search(data, query)
	print 'QUERY: ',query
	resList = []
	# print results
	for key in results.keys():
		if(results[key]['specs'].has_key("Item model number")):
			if (request.POST['query_term'].lower() in results[key]['specs']['Item model number'].lower()) or (results[key]['specs']['Item model number'].lower() in request.POST['query_term'].lower()):
				sents = results[key]['sent']
				vsents = [float(v) for v in sents]
				sumsents = sum(vsents)
				print sumsents
				nsents = [0.0,0.0,0.0,0.0,0.0]
				if(sumsents > 0):
					nsents = [(i*100)/sumsents for i in vsents]
				results[key]['sent'] = nsents
				resList.append(results[key])
				print nsents
		# print results[key]['specs']
	resList.sort(key=lambda x:x['avg rating'], reverse=True)
	return render(request, 'search_results.html', {'summary':resList})
	# return HttpResponse(len(results.keys()))
	# return HttpResponseRedirect(reverse('app:search_results', args=()))

def search_results(request):
	summary = [1,5,3,4,5,6]
		# return render(request, 'tldr/summary.html', { 'summary': summary })
	
