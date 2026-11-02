from django import forms
from .models import Company, Lead

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name','industry','email','phone','website','city','notes']
        widgets = {'notes': forms.Textarea(attrs={'rows':3})}

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name','email','phone','company','status','source','notes']
        widgets = {'notes': forms.Textarea(attrs={'rows':3})}
    def __init__(self, *args, owner=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(owner=owner) if owner else Company.objects.none()
        self.fields['status'].choices = [(k,v) for k,v in Lead.Status.choices if k != Lead.Status.CONVERTED]
        if self.instance.pk and self.instance.status == Lead.Status.CONVERTED:
            self.fields['status'].disabled = True
