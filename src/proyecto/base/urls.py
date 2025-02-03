from django.urls import path
from .views import ListaPendientes, DetalleTarea, CrearTarea, EditarTarea, EliminarTarea, Logueo, Registro, \
    CrearCategoria, CrearEtiqueta, ListaCategoria, ListaEtiqueta, EditarCategoria, EditarEtiqueta, EliminarCategoria, \
    ELiminarEtiqueta
from django.contrib.auth.views import LogoutView

urlpatterns = [path('',ListaPendientes.as_view(), name='tareas'),
               path('tarea/<int:pk>',DetalleTarea.as_view(), name='tarea'),
               path('crear-tarea/',CrearTarea.as_view(), name='crear-tarea'),
               path('editar/tarea/<int:pk>',EditarTarea.as_view(), name='editar-tarea'),
               path('eliminar/tarea/<int:pk>',EliminarTarea.as_view(), name='eliminar-tarea'),
               path('login/', Logueo.as_view(), name = 'login'),
               path('logout/', LogoutView.as_view(), name = 'logout'),
               path('registro/', Registro.as_view(), name = 'registro'),
               path('crear/categoria/', CrearCategoria.as_view(), name='crear-categoria'),
               path('crear/etiqueta/', CrearEtiqueta.as_view(), name='crear-etiqueta'),
               path('categorias/', ListaCategoria.as_view(), name='categoria-lista'),
               path('etiquetas/', ListaEtiqueta.as_view(), name= 'etiqueta-lista'),
               path('editar/categoria/<int:pk>', EditarCategoria.as_view(), name='editar-categoria'),
               path('editar/etiqueta/<int:pk>', EditarEtiqueta.as_view(), name='editar-etiqueta'),
               path('eliminar/categoria/<int:pk>', EliminarCategoria.as_view(), name='eliminar-categoria'),
               path('eliminar/etiqueta/<int:pk>', ELiminarEtiqueta.as_view(), name= 'eliminar-etiqueta')
               ]