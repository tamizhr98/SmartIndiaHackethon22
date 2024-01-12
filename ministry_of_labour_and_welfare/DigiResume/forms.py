from .models import *
from django import forms


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ['uid']
        #fields=['name','aadhar','photo','dob','gender','street','district','state','pincode','email','mobile','nationality']
        widgets = {
            'gender':forms.RadioSelect(choices=[
                ('Male','Male'),
                ('Female','Female'),
                ('Other','Other')
            ])
        }



class AddCourseForm(forms.ModelForm):

    def __init__(self, code, *args, **kwargs):
        super(AddCourseForm,self).__init__(*args, **kwargs)
        self.fields['uid'] = forms.CharField(max_length=16)
        self.fields['course_name'] = forms.ChoiceField(choices = tuple([(i.course_name,i.course_name) for i in courses.objects.filter(inst_code=code)]))

    class Meta:
        model = EducationInfo
        exclude = ['inst_code','uid']


        



class AddWorkOrganisationForm(forms.ModelForm):
    def __init__(self, code, *args, **kwargs):
        super(AddWorkOrganisationForm,self).__init__(*args, **kwargs)
        self.fields['uid'] = forms.CharField(max_length=16)
        self.fields['role'] = forms.ChoiceField(choices = tuple([(i.role_name,i.role_name) for i in RolesByOrganisation.objects.filter(org_code=code)]))

    class Meta:
        model = WorkInfoByOrganisation
        exclude = ['org_code','resign_date','uid']


class AddWorkInstitutionForm(forms.ModelForm):
    def __init__(self, code, *args, **kwargs):
        super(AddWorkInstitutionForm,self).__init__(*args, **kwargs)
        self.fields['uid'] = forms.CharField(max_length=16)
        self.fields['role'] = forms.ChoiceField(choices = tuple([(i.role_name,i.role_name) for i in RolesByInstitution.objects.filter(inst_code=code)]))
    
    class Meta:
        model = WorkInfoByInstitution
        exclude = ['inst_code','resign_date','uid']


class AddUnorganisedWorkForm(forms.ModelForm):
    class Meta:
        model = UnorganisedWorkInfo
        exclude = ['seva_code']
        