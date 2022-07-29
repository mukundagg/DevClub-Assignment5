# Generated by Django 4.0.6 on 2022-07-13 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Quizzes', '0001_initial'),
        ('Documents', '0001_initial'),
        ('Grades', '0008_alter_assignment_earntmarks_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='notes',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='quiz',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Quizzes.quiz'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='remarks',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='submission',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usersubmission', to='Documents.docs'),
        ),
    ]
