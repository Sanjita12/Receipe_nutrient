# Generated by Django 2.1.5 on 2019-02-23 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('NDB_No', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('FdGrp_Cd', models.CharField(max_length=4)),
                ('Long_Desc', models.CharField(max_length=200)),
                ('Shrt_Desc', models.CharField(max_length=60)),
                ('ComName', models.CharField(blank=True, max_length=100, null=True)),
                ('ManufacName', models.CharField(blank=True, max_length=65, null=True)),
                ('Survey', models.CharField(blank=True, max_length=1, null=True)),
                ('Ref_desc', models.CharField(blank=True, max_length=135, null=True)),
                ('Refuse', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('SciName', models.CharField(blank=True, max_length=65, null=True)),
                ('N_Factor', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('Pro_Factor', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('Fat_Factor', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('CHO_Factor', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Nutrient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nutr_No', models.CharField(max_length=3)),
                ('Nutr_Val', models.DecimalField(decimal_places=3, max_digits=10)),
                ('Std_Error', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('Deriv_Cd', models.CharField(blank=True, max_length=4, null=True)),
                ('Ref_NDB_No', models.CharField(blank=True, max_length=5, null=True)),
                ('Add_Nutr_Mark', models.CharField(blank=True, max_length=1, null=True)),
                ('NDB_No', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nutrient.Ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Weight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Seq', models.CharField(max_length=3)),
                ('Msre_Desc', models.CharField(max_length=84, null=True)),
                ('Amount', models.DecimalField(decimal_places=3, max_digits=5)),
                ('Gm_Wgt', models.DecimalField(decimal_places=1, max_digits=7)),
                ('Std_Dev', models.DecimalField(blank=True, decimal_places=3, max_digits=7, null=True)),
                ('NDB_No', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nutrient.Ingredient')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='weight',
            unique_together={('NDB_No', 'Seq')},
        ),
        migrations.AlterUniqueTogether(
            name='nutrient',
            unique_together={('NDB_No', 'Nutr_No')},
        ),
    ]
