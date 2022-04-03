from django.http import HttpResponse
from zenplayer.interaction import ZenFetcher
from django.views.generic.base import TemplateView


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class UIView(TemplateView):

    template_name = "ui.html"

    def get_context_data(self, **kwargs):
        context = super(UIView, self).get_context_data(**kwargs)
        for key, value in ZenFetcher.now_playing().items():
            context[key] = value
        return context
