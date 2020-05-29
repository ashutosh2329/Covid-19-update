from django.shortcuts import render
from django.views.generic import View
# Create your views here.



class Global(View):
    mytemplate = 'global_status.html'
    unsupported = 'Unsupported operation'
    def get(self, request):

        context = {
            'message':"Success",
        }
        return render(request,self.mytemplate,context)

    def post(self, request):
        return HttpResponse(self.unsupported)

class Covid19(View):
    mytemplate = 'covid19.html'
    unsupported = 'Unsupported operation'
    def get(self, request):

        context = {
            'message':"Success",
        }
        return render(request,self.mytemplate,context)

    def post(self, request):
        return HttpResponse(self.unsupported)
