# Generated by Django 4.0.6 on 2022-07-27 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quizzes', '0004_alter_quiz_earntmarks_alter_quiz_maxmarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='marks',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='qnNo',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='questionbank',
            name='summarks',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
