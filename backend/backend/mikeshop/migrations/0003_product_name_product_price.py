# Generated by Django 5.1.1 on 2024-09-16 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mikeshop', '0002_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
    ]
