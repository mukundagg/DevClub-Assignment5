# Generated by Django 4.0.6 on 2022-07-28 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fromMsg', models.CharField(blank=True, default='#', max_length=12)),
                ('toMsg', models.CharField(blank=True, default='#', max_length=12)),
                ('content', models.CharField(blank=True, max_length=50000)),
            ],
        ),
    ]
