from django.db import models

# Create your models here.
class Operacion(models.Model):
    numero1 = models.IntegerField()
    numero2 = models.IntegerField()
    resultado = models.IntegerField(blank=True, null=True)
    operador = models.CharField(max_length=10)
