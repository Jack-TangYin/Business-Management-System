# Generated by Django 5.1.2 on 2024-11-02 18:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_alter_staff_joining_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('status', models.CharField(choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('On Hold', 'On Hold'), ('Canceled', 'Canceled')], default='Not Started', max_length=20, verbose_name='Status')),
                ('priority', models.CharField(blank=True, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'), ('Urgent', 'Urgent')], max_length=10, null=True, verbose_name='Priority')),
                ('assigned_department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.department', verbose_name='Assigned Department')),
                ('assigned_staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.staff', verbose_name='Assigned Staff')),
            ],
        ),
    ]
