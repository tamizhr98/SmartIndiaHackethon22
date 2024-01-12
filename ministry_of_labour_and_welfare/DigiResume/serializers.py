from rest_framework import serializers
from .models import *

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class EducationInfoSerializer(serializers.ModelSerializer):
    inst_name = serializers.SerializerMethodField('getInstName')
    class Meta:
        model = EducationInfo
        fields = ['inst_name','course_name','completion_date','grade']
    
    def getInstName(self, EducationInfo):
        return EducationInfo.inst_code.inst_name

class WorkInfoByInstitutionSerializer(serializers.ModelSerializer):
    inst_name = serializers.SerializerMethodField('getInstName')
    class Meta:
        model = WorkInfoByInstitution
        fields = ['inst_name', 'role', 'join_date', 'resign_date']

    def getInstName(self, WorkInfoByInstitution):
        return WorkInfoByInstitution.inst_code.inst_name

class WorkInfoByOrganisationSerializer(serializers.ModelSerializer):
    org_name = serializers.SerializerMethodField('getOrgName')
    class Meta:
        model = WorkInfoByOrganisation
        fields = ['org_name', 'role', 'join_date', 'resign_date']

    def getOrgName(self, WorkInfoByOrganisation):
        return WorkInfoByOrganisation.org_code.org_name

class UnorganisedWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnorganisedWorkInfo
        exclude = ['seva_code']


