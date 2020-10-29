from django import forms
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from .models import  Organization, Request
from users.models import Permissions

class OrganizationJoinRequestForm(forms.Form):

    slug = forms.SlugField(label="", max_length=5)
    id = forms.IntegerField(label="", min_value=1)

    def clean(self):

        cleaned_data = super().clean()
        try:
            organization = Organization.objects.get(pk=cleaned_data.get("id"))
            if not organization or not slugify(organization.name[:5]) == cleaned_data.get("slug"):
                raise
        except:
            raise ValidationError("Invalid organization code.")


class PermissionsForm(forms.ModelForm):
    class Meta:
        model = Permissions
        exclude = ('user',)

class MemberDeleteForm(forms.Form):

    user = forms.IntegerField(widget=forms.HiddenInput)
