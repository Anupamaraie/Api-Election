# Generated by Django 4.1.3 on 2022-11-18 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Main',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Election_Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('election_area', models.CharField(max_length=100)),
                ('time', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='data', to='e_app.main')),
            ],
        ),
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('party', models.CharField(max_length=100)),
                ('vote', models.IntegerField()),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='candidates', to='e_app.election_area')),
            ],
        ),
    ]
