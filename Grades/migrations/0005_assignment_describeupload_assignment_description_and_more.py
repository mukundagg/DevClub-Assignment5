# Generated by Django 4.0.6 on 2022-07-13 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Documents', '0001_initial'),
        ('Grades', '0004_alter_assignment_duedate'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='describeUpload',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Documents.docs'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='description',
            field=models.CharField(blank=True, default='No Description Provided', max_length=50000),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='submission',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='usersubmission', to='Documents.docs'),
        ),
    ]
