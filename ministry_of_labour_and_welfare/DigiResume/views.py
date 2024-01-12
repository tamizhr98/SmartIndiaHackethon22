
from email import message
from logging import exception
from django.shortcuts import redirect, render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from .serializers import *
from .models import *
from .utilities import *
from .forms import *

# Create your views here.

#api 




class API(APIView):
    def get(self, request, uid):
        p = Person.objects.get(uid = uid)
        e = EducationInfo.objects.filter(uid=uid)
        wo = WorkInfoByOrganisation.objects.filter(uid=uid)
        wi = WorkInfoByInstitution.objects.filter(uid=uid)
        uw = UnorganisedWorkInfo.objects.filter(uid = uid)
        serializer ={ 'details': PersonSerializer(p).data , 'education' : EducationInfoSerializer(e, many=True).data, 'work ' : WorkInfoByInstitutionSerializer(wi, many=True).data + WorkInfoByOrganisationSerializer(wo, many=True).data }
        #serializer = EducationInfoSerializer(e, many=True)
        return Response(serializer)






#--------------------------------------------------------------------------------------------#


def index(request):
    message = ''
    if request.GET:
        try:
            uid=request.GET.dict()['id'].upper()
            return redirect(f'/{uid}/view_details')
        except:
            message = 'user does not exit'
    return render(request,'DigiResume/index.html')

def loginQR(request):
    uid = qrDetector()
    return redirect(f'/{uid}/view_details')



def login(request):
    message = ''
    flag=True
    if request.GET:
        id=request.GET.dict()['id'].upper()
        password=request.GET.dict()['password']
        global sector
        try:
            if 'EDU' in id:
                sector=1
                x=Institution.objects.get(inst_code=id).password
            elif 'ORG' in id:
                sector=2
                x=Organisation.objects.get(org_code=id).password
            elif 'SEV' in id:
                sector=3
                x=SevaStore.objects.get(seva_code=id).password
            if password==x:
                return redirect(f'/{id}/home/')
            else:
                flag=False
        except:
            message = 'user does not exist'
    return render(request,'DigiResume/login.html',{'flag':flag, 'message' : message})






def home(request,code):
    if sector==1:
        x=Institution.objects.get(inst_code=code)
    elif sector==2:
        x=Organisation.objects.get(org_code=code)        
    elif sector==3:
        x=SevaStore.objects.get(seva_code=code)
    return render(request,'DigiResume/home.html',{'sector':sector,'code':code,'x':x})





def register(request,code):
    uid=generateUID()
    message = None
    if uid in Person.objects.values_list('uid',flat=True):
        return register(request,code)

    if request.method == 'POST':
            form = RegisterForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    obj=form.save(commit=False)
                    obj.uid=uid
                    obj.save()
                    #card gen
                    card=generateCard(uid)
                    card.show()
                    InstitutionActivity(uid=Person(uid = uid), inst_code = Institution(inst_code=code), action = f'User resistered {uid}').save()
                except:
                    message = 'card already generated'
                #updating activity table
                return HttpResponse(f"""User resistered {uid}<br><a><img src=""/></a>""")
    else:
        form = RegisterForm()
    return render(request,'DigiResume/register.html',{'form':form,'sector':sector,'code':code, 'message' :message})






def add_course(request,code):
    if request.method == 'POST':
            form = AddCourseForm(code, request.POST)
            if form.is_valid():
                request.session['uid'] = form.cleaned_data['uid']
                request.session['course_name'] = form.cleaned_data['course_name']
                request.session['completion_date'] = str(form.cleaned_data['completion_date'])
                request.session['grade'] = form.cleaned_data['grade']
                return redirect(f'/{code}/add_course/confirm')
    else:
        form = AddCourseForm(code)  
    return render(request,'DigiResume/add_course.html',{'code':code,'sector':sector,'form':form})


def add_course_qr(request,code):
    uid =''
    message = None
    try:
        uid = qrDetector()
    except:
        message ='cam not found'
    if request.method == 'POST':
        form = AddCourseForm(code, request.POST)
        if form.is_valid():
            request.session['uid'] = form.cleaned_data['uid']
            request.session['course_name'] = form.cleaned_data['course_name']
            request.session['completion_date'] = str(form.cleaned_data['completion_date'])
            request.session['grade'] = form.cleaned_data['grade']
            return redirect(f'/{code}/add_course/confirm')
    else:
        form = AddCourseForm(code, initial = {'uid': uid})  
    return render(request,'DigiResume/add_course.html',{'code':code,'sector':sector,'form':form, 'message':message})

def confirmAddCourse(request,code):
    message = ''
    obj = EducationInfo()
    uid = request.session['uid']
    obj.uid = Person(uid = uid)
    obj.inst_code = Institution(inst_code=code)
    course_name = request.session['course_name']
    obj.course_name = course_name
    obj.completion_date = request.session['completion_date']
    obj.grade = request.session['grade']
    if request.POST:
        try:
            obj.save()
            InstitutionActivity(uid=Person(uid = uid),
            inst_code = Institution(inst_code=code),
            action = f'{course_name} Course Added for {uid}').save()
        except:
            message = 'course already added'
        return HttpResponse(f'{course_name} Course Added for {uid}')
    return render(request,'DigiResume/confirm.html',{'x' : Person.objects.get(uid=uid), 'message':message})




def add_work(request,code):    
    if sector==1:    
        if request.method == 'POST':
            form = AddWorkInstitutionForm(code, request.POST)
            if form.is_valid():
               request.session['uid'] = form.cleaned_data['uid']
               request.session['role'] = form.cleaned_data['role']
               request.session['join_date'] = str(form.cleaned_data['join_date'])
               return redirect(f'/{code}/add_work/confirm')
        else:
            form = AddWorkInstitutionForm(code)
            
    elif sector==2:
        if request.method == 'POST':
            form = AddWorkOrganisationForm(code, request.POST)
            if form.is_valid():
               request.session['uid'] = form.cleaned_data['uid']
               request.session['role'] = form.cleaned_data['role']
               request.session['join_date'] = str(form.cleaned_data['join_date'])
               return redirect(f'/{code}/add_work/confirm')
   
        else:
            form = AddWorkOrganisationForm(code)

    elif sector==3:
        if request.method == 'POST':
            form = AddUnorganisedWorkForm(request.POST)
            if form.is_valid():
                uid = form.cleaned_data['uid']
                work = form.cleaned_data['work_name']
                SevaActivity(uid=Person(uid = uid), seva_code = SevaStore(seva_code=code), action = f'{work} work Added for {uid}').save()
                obj = form.save(commit = False)
                obj.seva_code = SevaStore(seva_code=code)
                obj.save()
                return HttpResponse(f'{work} work Added for {uid}')
        else:
            form = AddUnorganisedWorkForm()            
    return render(request,'DigiResume/add_work.html',{'code':code,'form':form, 'sector':sector})






def add_work_qr(request,code):
    uid =''
    message = None
    if request.method != 'POST':
        try:
            uid = qrDetector()
        except:
            message ='cam not found'    
    if sector==1:    
        if request.method == 'POST':
            form = AddWorkInstitutionForm(code, request.POST)
            if form.is_valid():
               request.session['uid'] = form.cleaned_data['uid']
               request.session['role'] = form.cleaned_data['role']
               request.session['join_date'] = str(form.cleaned_data['join_date'])
               return redirect(f'/{code}/add_work/confirm')
        else:
            form = AddWorkInstitutionForm(code, initial={'uid':uid})
            
    elif sector==2:
        if request.method == 'POST':
            form = AddWorkOrganisationForm(code, request.POST)
            if form.is_valid():
               request.session['uid'] = form.cleaned_data['uid']
               request.session['role'] = form.cleaned_data['role']
               request.session['join_date'] = str(form.cleaned_data['join_date'])
               return redirect(f'/{code}/add_work/confirm')
   
        else:
            form = AddWorkOrganisationForm(code, initial={'uid':uid})

    elif sector==3:
        if request.method == 'POST':
            form = AddUnorganisedWorkForm(request.POST)
            if form.is_valid():
                uid = form.cleaned_data['uid']
                work = form.cleaned_data['work_name']
                SevaActivity(uid=Person(uid = uid), seva_code = SevaStore(seva_code=code), action = f'{work} work Added for {uid}').save()
                obj = form.save(commit = False)
                obj.seva_code = SevaStore(seva_code=code)
                obj.save()
                return HttpResponse(f'{work} work Added for {uid}')
        else:
            form = AddUnorganisedWorkForm(initial={'uid':uid})            
    return render(request,'DigiResume/add_work.html',{'code':code,'form':form, 'sector':sector, 'message':message})


def confirmAddWork(request, code):
    uid = request.session['uid']
    if sector==1:
        role = request.session['role']
        obj = WorkInfoByInstitution()
        obj.uid = Person(uid = uid)
        obj.inst_code = Institution(inst_code = code)
        obj.role = role
        obj.join_date = request.session['join_date']
        obj.resign_date = None
        if request.POST:
            obj.save()
            InstitutionActivity(uid=Person(uid = Person(uid=uid)), inst_code = Institution(inst_code=code), action = f'{role} work Added for {uid}').save()
            return HttpResponse(f'{role} work Added for {uid}')
        
    elif sector==2:
        role = request.session['role']
        obj = WorkInfoByOrganisation()
        obj.uid = Person(uid = uid)
        obj.org_code = Organisation(org_code = code)
        obj.role = request.session['role']
        obj.join_date = request.session['join_date']
        obj.resign_date = None
        if request.POST:
            obj.save()
            OrganisationActivity(uid=Person(uid = uid), org_code = Organisation(org_code=code), action = f'{role} work Added for {uid}').save()
            return HttpResponse(f'{role} work Added for {uid}')

        elif sector==3:
            pass
    return render(request,'DigiResume/confirm.html',{'x' : Person.objects.get(uid=uid)})





def add_resign(request,code):
    if request.GET:
        request.session['uid'] = request.GET.dict()['uid']
        if sector==1:
            request.session['resign_date'] = str(request.GET.dict()['resign_date'])
            return redirect(f'/{code}/add_resign/confirm')

        elif sector==2:
            request.session['resign_date'] =str(request.GET.dict()['resign_date'])
            return redirect(f'/{code}/add_resign/confirm')

    else:
        o=''
    return render(request,'DigiResume/add_resign.html',{'code': code,'o':o, 'sector':sector})


def add_resign_qr(request,code):
    uid =''
    message = None
    if not request.GET:
        try:
            uid = qrDetector()
        except:
            message ='cam not found'
    if request.GET:
        request.session['uid'] = request.GET.dict()['uid']
        if sector==1:
            request.session['resign_date'] =str(request.GET.dict()['resign_date'])
            return redirect(f'/{code}/add_resign/confirm')

        elif sector==2:
            request.session['resign_date'] =str(request.GET.dict()['resign_date'])
            return redirect(f'/{code}/add_resign/confirm')

    else:
        o=''
    return render(request,'DigiResume/add_resign.html',{'code': code,'o':o, 'sector':sector, 'uid':uid, 'message':message})



def confirmAddResign(request, code):
    uid = request.session['uid']
    message = ''
    if sector==1:
        if request.POST:
            try:
                obj = WorkInfoByInstitution.objects.get(uid=uid, inst_code=code)
                role = obj.role
                obj.resign_date = request.session['resign_date']
                obj.save()
                InstitutionActivity(uid=Person(uid = Person(uid=uid)), inst_code = Institution(inst_code=code), action = f'{role} resign date Added for {uid}').save()
                return HttpResponse(f'{role} resign date Added for {uid}')
            except:
                message ='no role enrolled'
    elif sector==2:
        if request.POST:
            try:
                obj = WorkInfoByOrganisation.objects.get(uid=uid, org_code=code)
                role = obj.role
                obj.resign_date = request.session['resign_date']
                obj.save()
                OrganisationActivity(uid=Person(uid = Person(uid=uid)), org_code = Organisation(org_code=code), action = f'{role} resign date Added for {uid}').save()
                return HttpResponse(f'{role} resign date Added for {uid}')
            except:
                message ='no role enrolled'        
    return render(request,'DigiResume/confirm.html',{'x' : Person.objects.get(uid=uid), 'message' : message})





def activity(request,code):
    if sector==1:
        o=InstitutionActivity.objects.filter(inst_code=code)
    if sector==2:
        o=OrganisationActivity.objects.filter(org_code=code)
    if sector==3:
        o=SevaActivity.objects.filter(seva_code=code)
    return render(request,'DigiResume/activity.html',{'code':code, 'o':o, 'sector':sector})





def view_details(request,uid):
    message =''
    x,y,z,a,uw ='','','','',''
    try:
        x=Person.objects.get(uid=uid)
        y=EducationInfo.objects.filter(uid=uid)
        z=WorkInfoByOrganisation.objects.filter(uid=uid)
        a = WorkInfoByInstitution.objects.filter(uid=uid)
        uw = UnorganisedWorkInfo.objects.filter(uid = uid)
    except:
        message = 'person does not exist'
    return render(request,'DigiResume/view_details.html',{'x':x,'y':y,'z':z,'a':a, 'uw':uw, 'message' : message})



def trace(request):
    x=''
    if request.GET:
        from_date = request.GET.dict()['from'] 
        to = request.GET.dict()['to']
        print(from_date)
        #in particular yr
        x = WorkInfoByOrganisation.objects.filter(join_date__gte=from_date, join_date__lte=to)
        return render(request,'DigiResume/trace.html',{'x': x})
    
        #not employed
        # x = WorkInfoByOrganisation.objects.exclude(resign_date = None )

        #not employed so far
    return render(request,'DigiResume/trace.html')