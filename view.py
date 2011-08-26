import sys
import inspect
from django.shortcuts import render_to_response
from django.template import RequestContext

class ViewException(Exception): pass

class View(object):
    def __init__(self):
        pass
    
    def __new__(cls, request, *args, **kwargs):
        obj = super(View, cls).__new__(cls)
        return obj(request, *args, **kwargs)

    def __call__(self, request, *args, **kwargs):
        self.request = request
        self.app =  inspect.getmodule(self).__name__.split('.')[-2]
        self.action = self.__class__.__name__

        if request.method == 'POST':
            if hasattr(self,'post') and callable(self.post):
                return self.post(*args, **kwargs)

        if request.method == 'GET':
            if hasattr(self,'get') and callable(self.get):
                return self.get(*args, **kwargs)

        if hasattr(self,'do') and callable(self.do):
            return self.do(*args, **kwargs)
        else:
            raise ViewException(u'View class must have method "do" ')

    def render_to_response(self, template_name, vars={}):
        vars['app'] = {'name': self.app, 'action':self.action}
        return render_to_response(
            template_name,
            vars,
            context_instance=RequestContext(self.request)
        )

