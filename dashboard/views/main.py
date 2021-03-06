from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import FormView
from dashboard.models import * 
from dashboard.forms import addTaskForm
import requests

class dashboardView(FormView):
    template_name = 'dashboard.html'
    form_class = addTaskForm
    success_url = '/'
    
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['recent_process']= processExecutions.objects.all().order_by('-id')
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        try:
            requests.get("http://139.59.30.183:8080/job/fetch_api_data/build?token=d3b5d9014ae241afad858b7d31c0c6a9")
        except:
            pass
        return super(self.__class__, self).form_valid(form)