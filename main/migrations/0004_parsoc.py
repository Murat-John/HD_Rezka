# Generated by Django 3.1 on 2021-03-15 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210313_1924'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParsOc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('photo', models.CharField(max_length=255)),
            ],
        ),
    ]
