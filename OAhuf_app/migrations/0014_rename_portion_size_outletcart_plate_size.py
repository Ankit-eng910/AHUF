# Generated by Django 5.2 on 2025-07-17 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OAhuf_app', '0013_outletcart_added_on_alter_outletcart_portion_size'),
    ]

    operations = [
        migrations.RenameField(
            model_name='outletcart',
            old_name='portion_size',
            new_name='plate_size',
        ),
    ]
