from django import forms

from gasapp.models import *


class AgencyRegistrationForm(forms.ModelForm):
  class Meta:
        model = AgencyTable
        fields = ['Agencyname', 'Phone', 'place']

class SafetyRegistrationForm(forms.ModelForm):
  class Meta:
        model = fireandsafety
        fields = [ 'Phone', 'place']
