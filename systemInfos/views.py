from django.http import HttpResponse
from django.template import loader

from .models import SystemInfo


def systeminfo(request):
    print("haha")
    systeminfo_list = SystemInfo()
    template = loader.get_template('systeminfos/systeminfos.html')
    context = {
        'systeminfo_list': systeminfo_list
    }
    return HttpResponse(template.render(context,request))