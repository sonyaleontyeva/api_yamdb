# Generated by Django 3.2 on 2023-06-14 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='title', to='titles.category'),
        ),
        migrations.AddField(
            model_name='title',
            name='description',
            field=models.TextField(default='desc'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='title', to='titles.genre'),
        ),
        migrations.AddField(
            model_name='title',
            name='name',
            field=models.CharField(default='name', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='title',
            name='rating',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='title',
            name='year',
            field=models.IntegerField(default=2010),
            preserve_default=False,
        ),
    ]
