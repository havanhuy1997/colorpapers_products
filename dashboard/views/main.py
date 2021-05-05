from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from dashboard.models import * 

class dashboardView(View):
    
    def __init__(self, **kwargs):
        self.template_name = {
            'main': "dashboard.html",
        }

    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        page_type = 'main'
        context_dict = {
            "recent_process": processExecutions.objects.all().order_by('-id')[:100]
        }

        return render(request, self.template_name[page_type], context_dict)
        # return HttpResponseRedirect(reverse('dashboard:opportunities'))