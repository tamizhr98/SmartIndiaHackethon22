# Generated by Django 4.1 on 2022-08-24 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DigiResume', '0011_alter_courses_course_name_alter_person_aadhar_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='aadhar',
            field=models.IntegerField(),
        ),
    ]
