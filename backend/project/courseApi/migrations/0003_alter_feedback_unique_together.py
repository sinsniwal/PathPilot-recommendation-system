# Generated by Django 4.2.7 on 2023-12-13 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courseApi', '0002_feedback_student'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='feedback',
            unique_together=set(),
        ),
    ]
