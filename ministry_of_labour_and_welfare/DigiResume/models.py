from django.db import models

# Create your models here.

#-----------------------------------------------------------------------#

#person table

class Person(models.Model):
    uid=models.CharField(max_length=16,primary_key=True)
    name=models.CharField(max_length=50)
    aadhar=models.IntegerField()
    photo=models.ImageField(upload_to='person/')
    dob=models.DateField()
    gender=models.CharField(max_length=6)
    street=models.CharField(max_length=50)
    district=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    pincode=models.IntegerField()
    email=models.CharField(max_length=30)
    mobile=models.IntegerField()
    nationality=models.CharField(max_length=10)


    def __str__(self):
        return str(self.uid)
#-----------------------------------------------------------------------#
#institution tables

class Institution(models.Model):
    inst_code=models.CharField(max_length=9,primary_key=True)
    password=models.CharField(max_length=16)
    inst_name=models.CharField(max_length=50)
    owner_name=models.CharField(max_length=50)
    owner_uid=models.CharField(max_length=16)
    street=models.CharField(max_length=20)
    district=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    pincode=models.IntegerField()
    email=models.CharField(max_length=30)
    mobile=models.IntegerField()



class courses(models.Model):
    inst_code=models.ForeignKey(Institution,on_delete=models.CASCADE)
    course_name=models.CharField(max_length=100)

class RolesByInstitution(models.Model):
    inst_code=models.ForeignKey(Institution,on_delete=models.CASCADE)
    role_name=models.CharField(max_length=100)



class InstitutionActivity(models.Model):
    date_time=models.DateTimeField(auto_now=True)
    uid=models.ForeignKey(Person,on_delete=models.CASCADE)
    inst_code=models.ForeignKey(Institution,on_delete=models.CASCADE)
    action=models.CharField(max_length=50)
    

#-----------------------------------------------------------------------#
#oraganisation tables

class Organisation(models.Model):
    org_code=models.CharField(max_length=9,primary_key=True)
    password=models.CharField(max_length=16)
    org_name=models.CharField(max_length=50)
    owner_name=models.CharField(max_length=50)
    owner_uid=models.CharField(max_length=16)
    street=models.CharField(max_length=20)
    district=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    pincode=models.IntegerField()
    email=models.CharField(max_length=30)
    mobile=models.IntegerField()

    def __str__(self):
        return self.org_code

class RolesByOrganisation(models.Model):
    org_code=models.ForeignKey(Organisation,on_delete=models.CASCADE)
    role_name=models.CharField(max_length=100)



class OrganisationActivity(models.Model):
    date_time=models.DateTimeField(auto_now=True)
    uid=models.ForeignKey(Person,on_delete=models.CASCADE)
    org_code=models.ForeignKey(Organisation,on_delete=models.CASCADE)
    action=models.CharField(max_length=50)

#-----------------------------------------------------------------------#
#seva stores for unorganised works

class SevaStore(models.Model):
    seva_code=models.CharField(max_length=9,primary_key=True)
    password=models.CharField(max_length=16)
    seva_name=models.CharField(max_length=50)
    owner_name=models.CharField(max_length=30)
    owner_uid=models.CharField(max_length=16)
    street=models.CharField(max_length=20)
    district=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    pincode=models.IntegerField()
    email=models.CharField(max_length=20)
    mobile=models.IntegerField()



class SevaActivity(models.Model):
    date=models.DateField(auto_now=True)
    uid=models.ForeignKey(Person,on_delete=models.CASCADE)
    seva_code=models.ForeignKey(SevaStore ,on_delete=models.CASCADE)
    action=models.CharField(max_length=50)


#-----------------------------------------------------------------------#
#person information

class EducationInfo(models.Model):
    # class Meta:
    #     unique_together = (('uid','inst_code','course_name'),)
    uid=models.ForeignKey(Person,on_delete=models.CASCADE,primary_key = False)
    inst_code=models.ForeignKey(Institution,on_delete=models.CASCADE)
    course_name=models.CharField(max_length=100)
    completion_date=models.DateField()
    grade=models.IntegerField()

class WorkInfoByOrganisation(models.Model):
    # class Meta:
    #     unique_together = (('uid','org_code','role'),)
    uid=models.ForeignKey(Person,on_delete=models.CASCADE)
    org_code=models.ForeignKey(Organisation,on_delete=models.CASCADE)
    role=models.CharField(max_length=100)
    join_date=models.DateField()
    resign_date=models.DateField(null=True,blank=True)


class WorkInfoByInstitution(models.Model):
    # class Meta:
    #     unique_together = (('uid','inst_code','role'),)
    uid=models.ForeignKey(Person,on_delete=models.CASCADE)
    inst_code=models.ForeignKey(Institution,on_delete=models.CASCADE)
    role=models.CharField(max_length=100)
    join_date=models.DateField()
    resign_date=models.DateField(null=True,blank=True)

class UnorganisedWorkInfo(models.Model):
    uid=models.ForeignKey(Person,on_delete=models.CASCADE)
    seva_code=models.ForeignKey(SevaStore,on_delete=models.CASCADE)
    work_name=models.CharField(max_length=200)

#-----------------------------------------------------------------------#
class resources(models.Model):
    name=models.CharField(max_length=10)
    img=models.ImageField(upload_to='resources/')


