# Generated by Django 4.2.7 on 2023-11-15 09:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("courseApi", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="level",
            field=models.CharField(
                choices=[
                    ("foundation", "Foundation"),
                    ("diploma", "Diploma"),
                    ("bsc", "Bsc"),
                    ("bs", "Bs"),
                ],
                default=django.utils.timezone.now,
                max_length=20,
            ),
            preserve_default=False,
        ),
    ]
