# Generated by Django 4.0.6 on 2022-07-29 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0008_course_coursebackground'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='profilephoto',
            field=models.ImageField(default='static/profile.png', upload_to='media/'),
        ),
    ]
