from django import forms
from .models import Site


class SiteCreateForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['name', 'url']
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(SiteCreateForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        if Site.objects.filter(user=self.user, name=name).exists():
            raise forms.ValidationError("You have already created a site with the same name.")
        return name
