# Generated by Django 3.0.6 on 2020-05-17 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='comuna',
            fields=[
                ('CodComuna', models.IntegerField(default=None, primary_key=True, serialize=False)),
                ('ComunaName', models.CharField(default=None, max_length=50)),
                ('Poblation', models.FloatField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='region',
            fields=[
                ('Codregion', models.CharField(default=None, max_length=2, primary_key=True, serialize=False)),
                ('RegionName', models.CharField(default=None, max_length=50)),
                ('Area', models.FloatField(default=None)),
                ('Lat', models.FloatField(default=None)),
                ('Long', models.FloatField(default=None)),
                ('Population', models.FloatField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='reportexcomuna',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=50)),
                ('cod_region', models.CharField(max_length=50)),
                ('comuna', models.CharField(default=None, max_length=50)),
                ('comunaCodComuna', models.CharField(max_length=50)),
                ('poblacion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='reportes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RDate', models.DateField(default=None)),
                ('RConfirmed', models.FloatField(default=None)),
                ('RActive', models.FloatField(default=None)),
                ('RComuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corona_app.comuna')),
            ],
        ),
        migrations.CreateModel(
            name='deathsporRegion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DDate', models.DateField(default=None)),
                ('Ddeaths', models.FloatField(default=None)),
                ('DCodRegion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corona_app.region')),
            ],
        ),
        migrations.AddField(
            model_name='comuna',
            name='Reg',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corona_app.region'),
        ),
        migrations.CreateModel(
            name='activesCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AcDate', models.DateField(default=None)),
                ('AcCantidad', models.FloatField(default=None)),
                ('AcCod_comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corona_app.comuna')),
            ],
        ),
    ]