# Generated by Django 5.0.7 on 2024-09-28 17:23

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job', models.CharField(max_length=15)),
                ('mbti', models.CharField(max_length=15)),
                ('scenario', models.TextField()),
                ('generated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
