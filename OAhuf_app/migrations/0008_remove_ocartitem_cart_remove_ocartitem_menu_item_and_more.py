# Generated by Django 5.2 on 2025-07-12 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OAhuf_app', '0007_alter_booking_mobile_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ocartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='ocartitem',
            name='menu_item',
        ),
        migrations.AlterUniqueTogether(
            name='outletcart',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='outletcart',
            name='booking',
        ),
        migrations.RemoveField(
            model_name='outletcart',
            name='menu_item',
        ),
        migrations.DeleteModel(
            name='OCart',
        ),
        migrations.DeleteModel(
            name='OCartItem',
        ),
        migrations.DeleteModel(
            name='OutletCart',
        ),
    ]
