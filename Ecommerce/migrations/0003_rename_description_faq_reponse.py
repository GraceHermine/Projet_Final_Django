# Generated by Django 5.2 on 2025-04-09 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerce', '0002_faq'),
    ]

    operations = [
        migrations.RenameField(
            model_name='faq',
            old_name='description',
            new_name='reponse',
        ),
    ]
