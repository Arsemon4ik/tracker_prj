# Generated by Django 4.2.1 on 2023-05-13 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('done', 'Виконане'), ('processing', 'В процессы'), ('scheduled', 'Заплановане')], default='scheduled', max_length=10),
        ),
    ]
