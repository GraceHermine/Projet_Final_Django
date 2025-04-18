# Generated by Django 5.2 on 2025-04-11 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerce', '0009_equipe'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipe',
            options={'verbose_name': 'Notre équipe', 'verbose_name_plural': 'Notre équipe'},
        ),
        migrations.AddField(
            model_name='produit',
            name='en_promotion',
            field=models.BooleanField(default=False, verbose_name='Produit en promotion'),
        ),
        migrations.AddField(
            model_name='produit',
            name='pour_slider',
            field=models.BooleanField(default=False, verbose_name='Afficher dans le slider'),
        ),
        migrations.AddField(
            model_name='produit',
            name='prix_promo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Prix promotionnel'),
        ),
    ]
