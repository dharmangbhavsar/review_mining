from django.shortcuts import render, get_object_or_404
from django.forms import modelformset_factory
from django.views.generic import View
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

#Migrated from FBVs to CBVs as CBVs handle get and post logic cleanly
#----DASHBOARD----
class index(View):
	template_name = 'review_mining/index.html'	
	
	def get(self, request):
		return render(request, self.template_name)
	
	def post(self,request):
		pass