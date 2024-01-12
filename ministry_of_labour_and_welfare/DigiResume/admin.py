from django.contrib import admin
from .models import * 

# Register your models here.

admin.site.register(Person)
admin.site.register(Institution)
admin.site.register(courses)
admin.site.register(RolesByInstitution)
admin.site.register(InstitutionActivity)
admin.site.register(Organisation)
admin.site.register(RolesByOrganisation)
admin.site.register(OrganisationActivity)
admin.site.register(SevaStore)
admin.site.register(SevaActivity)
admin.site.register(EducationInfo)
admin.site.register(WorkInfoByOrganisation)
admin.site.register(WorkInfoByInstitution)
admin.site.register(UnorganisedWorkInfo)

admin.site.register(resources)