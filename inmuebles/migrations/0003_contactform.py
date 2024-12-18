# Generated by Django 5.1.3 on 2024-11-19 18:30

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0002_inmueble_fecha_creacion_inmueble_ultima_modificacion_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_form_uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('customer_name', models.CharField(max_length=64)),
                ('customer_email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
            ],
        ),
    ]
