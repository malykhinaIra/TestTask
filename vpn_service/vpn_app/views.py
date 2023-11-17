from django.urls import reverse
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.generic import TemplateView, ListView, CreateView
from .forms import SiteCreateForm
from .models import Site
from .services import make_internal


class SiteListView(ListView):
    template_name = 'site_list.html'
    model = Site
    context_object_name = 'sites'
    paginate_by = 10

    def get_queryset(self):
        return Site.objects.filter(user=self.request.user.id)


class ProxySiteView(View):
    template_name = 'proxy_site.html'

    def get(self, request, site_name, site_url=''):
        user_site = Site.objects.filter(user=request.user, name=site_name).first()

        if user_site:
            soup_obj = make_internal(request, user_site, site_name, site_url)
            return HttpResponse(str(soup_obj))

        else:
            messages.warning(request, f'Cannot access URL')
            return HttpResponseRedirect(reverse('proxy:site_list'))


class CreateSiteView(CreateView):
    template_name = 'create_site.html'
    form_class = SiteCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(reverse('proxy:site_list'))

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(CreateSiteView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs


class StatisticsView(TemplateView):
    template_name = 'statistics.html'

    def get_context_data(self, *args, **kwargs):
        context = super(StatisticsView, self).get_context_data(**kwargs)

        sites = Site.objects.filter(user=self.request.user.id)
        context['sites'] = sites

        return context
