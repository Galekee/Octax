from django import forms
from .models import Project,Sprint,WorkItem
class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project; fields=['name','goal','wip_limit']
        widgets={'goal':forms.Textarea(attrs={'rows':3})}
class SprintForm(forms.ModelForm):
    class Meta:
        model=Sprint; fields=['name','goal','start_date','end_date','retrospective','improvement','improvement_owner']
        widgets={'start_date':forms.DateInput(attrs={'type':'date'}),'end_date':forms.DateInput(attrs={'type':'date'}),'goal':forms.Textarea(attrs={'rows':2}),'retrospective':forms.Textarea(attrs={'rows':3})}
    def clean(self):
        d=super().clean()
        if d.get('start_date') and d.get('end_date') and d['end_date'] < d['start_date']:
            raise forms.ValidationError('Дата окончания должна быть после начала.')
        return d
class WorkItemForm(forms.ModelForm):
    class Meta:
        model=WorkItem; fields=['title','description','sprint','assignee']
        widgets={'description':forms.Textarea(attrs={'rows':3})}
    def __init__(self,*args,project=None,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['sprint'].queryset=Sprint.objects.filter(project=project) if project else Sprint.objects.none()
