# Generated by Django 4.2.7 on 2023-11-05 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_category_options_alter_file_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to='files/%Y/%m/%d/', verbose_name='file'),
        ),
        migrations.AlterField(
            model_name='file',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='product'),
        ),
    ]