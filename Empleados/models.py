# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
class Empleado(models.Model):
    clave = models.CharField(max_length=4, unique=True)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    edad = models.IntegerField()
    salario = models.FloatField()
    comentarios = models.CharField(max_length=1000)
    activo = models.IntegerField(default=1)
    fecha_ultima_actividad = models.DateTimeField(null=True, blank=True)