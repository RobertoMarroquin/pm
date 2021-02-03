# Generated by Django 3.1.1 on 2020-09-21 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0004_cuentaprincipal_catalogo'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcuenta',
            name='catalogo',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='general.catalogocuentas'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subcuenta',
            name='cuenta_principal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='general.cuentaprincipal', verbose_name='Cuenta Principal'),
        ),
    ]
