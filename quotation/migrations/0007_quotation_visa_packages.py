# Generated by Django 4.2.11 on 2024-06-15 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quotation', '0006_visapackage_remove_quotation_number_of_visa_packages_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='visa_packages',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quotation.visapackage'),
        ),
    ]