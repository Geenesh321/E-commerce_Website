# Generated by Django 4.2.3 on 2023-07-15 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0005_alter_cartproduct_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='city',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='customer',
            name='country',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(default=None, max_length=254),
        ),
        migrations.AddField(
            model_name='customer',
            name='last_name',
            field=models.CharField(default=None, max_length=150),
        ),
        migrations.AddField(
            model_name='customer',
            name='phone',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AddField(
            model_name='customer',
            name='pin_code',
            field=models.CharField(default=None, max_length=10),
        ),
        migrations.AddField(
            model_name='customer',
            name='state',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(default=None, max_length=150),
        ),
    ]