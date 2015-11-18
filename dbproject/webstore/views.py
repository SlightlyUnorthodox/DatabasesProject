from django.http import HttpResponse, HttpResponseRedirect
#from django.shortcuts import render, render_to_response
#from django.template import RequestContext

def index(request):
	return HttpResponse("Welcome to [name of webstore here]'s index.")
