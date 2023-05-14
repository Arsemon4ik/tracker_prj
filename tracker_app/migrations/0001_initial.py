# Generated by Django 4.2.1 on 2023-05-13 13:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True)),
                ('max_score', models.PositiveIntegerField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('score', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('deadline', models.DateTimeField(blank=True)),
                ('subject', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='tracker_app.subject', verbose_name='subjects')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]