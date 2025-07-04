# Generated by Django 5.2.1 on 2025-05-20 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_product_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='unit',
            field=models.CharField(choices=[('kg', 'Kilogram'), ('g', 'Gram')], default='kg', max_length=10),
        ),
    ]
