# Generated by Django 5.2 on 2025-07-18 12:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ahuf_app', '0002_alter_cartitem_unique_together_cartitem_plate_option_and_more'),
        ('OAhuf_app', '0017_booking_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='outlet_cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='OAhuf_app.outletcart'),
        ),
    ]
