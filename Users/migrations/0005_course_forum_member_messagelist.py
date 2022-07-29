# Generated by Django 4.0.6 on 2022-07-28 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Messages', '0006_forum_name'),
        ('Users', '0004_alter_member_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='forum',
            field=models.ManyToManyField(blank=True, to='Messages.forum'),
        ),
        migrations.AddField(
            model_name='member',
            name='messagelist',
            field=models.ManyToManyField(blank=True, to='Messages.forum'),
        ),
    ]
