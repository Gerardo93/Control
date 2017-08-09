# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import RedirectView, TemplateView, CreateView, UpdateView, DeleteView, ListView
from django.views.generic.edit import BaseUpdateView

from Empleados.models import Empleado

class HomeRedirect(RedirectView):
    permanent = False
    query_string = False

    def get_redirect_url(self):
        return reverse('empleados:empleados_list')

class EmpleadosList(ListView):

    def get(self, request, *args, **kwargs):
        empleados = Empleado.objects.all()
        request.opcionRender = 1
        return render(request, 'empleados/empleados.html', {
            'empleados': empleados
        })

campos = ['clave',
          'nombre',
          'apellido_paterno',
          'apellido_materno',
          'fecha_nacimiento',
          'edad',
          'salario',
          'comentarios',
          'activo'
          ]
class EmpleadosCreate(CreateView):
    model = Empleado
    success_url = reverse_lazy('empleados:empleados_list')
    fields = campos
    template_name = 'empleados/empleados.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        request.formOpcion = 'Crear'
        request.opcionRender = 2
        return super(EmpleadosCreate, self).get(request, *args, **kwargs)

class EmpleadosUpdate(UpdateView):
    model = Empleado
    success_url = reverse_lazy('empleados:empleados_list')
    fields = campos
    template_name = 'empleados/empleados.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        request.formOpcion = 'Editar'
        request.opcionRender = 2
        if self.object.activo == 1:
            return super(EmpleadosUpdate, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(self.success_url)

class EmpleadosDelete(DeleteView):
    model = Empleado
    success_url = reverse_lazy('empleados:empleados_list')
    template_name = 'empleados/empleados.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.activo == 1:
            request.formOpcion = 'inactivar'
            request.formOpcionB = 'Borrar'
        else:
            request.formOpcion = 'activar'
            request.formOpcionB = 'Restaurar'
        request.opcionRender = 3
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        if request.user.is_superuser:
            empleado = Empleado.objects.get(id=self.object.id)
            if empleado.activo == 1:
                empleado.activo = 0
                empleado.fecha_ultima_actividad = datetime.now()
            else:
                empleado.activo = 1
                empleado.fecha_ultima_actividad = None
            empleado.save()
        return HttpResponseRedirect(success_url)