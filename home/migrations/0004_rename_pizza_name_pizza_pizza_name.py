# Generated by Django 4.1 on 2022-08-12 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_cart_uid_alter_cartitems_uid_alter_pizza_uid_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pizza',
            old_name='Pizza_name',
            new_name='pizza_name',
        ),
    ]
