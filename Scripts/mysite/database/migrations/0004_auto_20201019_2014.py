# Generated by Django 3.1 on 2020-10-20 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_auto_20201018_1651'),
    ]

    operations = [
        migrations.CreateModel(
            name='PowerPlant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=10)),
                ('so_2', models.IntegerField()),
                ('c_no', models.IntegerField()),
                ('c_co2', models.IntegerField()),
                ('c_hg', models.IntegerField()),
                ('lat', models.CharField(max_length=30)),
                ('long', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'powerplants',
            },
        ),
        migrations.AlterModelOptions(
            name='vehicle',
            options={'verbose_name_plural': 'vehicles'},
        ),
    ]
