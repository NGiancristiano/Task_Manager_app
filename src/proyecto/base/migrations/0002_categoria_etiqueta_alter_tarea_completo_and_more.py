# Generated by Django 5.2a1 on 2025-02-03 10:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Etiqueta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='tarea',
            name='completo',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='tarea',
            name='creado',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='tarea',
            name='titulo',
            field=models.CharField(db_index=True, max_length=200),
        ),
        migrations.AddField(
            model_name='tarea',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.categoria'),
        ),
        migrations.AddField(
            model_name='tarea',
            name='etiquetas',
            field=models.ManyToManyField(blank=True, to='base.etiqueta'),
        ),
    ]
