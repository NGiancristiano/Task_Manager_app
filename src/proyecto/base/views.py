from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from .models import Tarea, Categoria, Etiqueta
from .forms import TareaForm, CategoriaForm, EtiquetaForm, UsuarioForm


class ListaPendientes(LoginRequiredMixin, ListView):
    model = Tarea
    context_object_name = 'tareas'

    def get_queryset(self):
        queryset = Tarea.objects.filter(usuario=self.request.user).select_related("usuario")


        # Filtrar por texto en titulo
        valor_buscado = self.request.GET.get('area-buscar') or ''
        if valor_buscado:
            queryset = queryset.filter(titulo__icontains=valor_buscado)

        # Filtrar por categoría
        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)

        # Filtrar por etiquetas
        etiqueta_id = self.request.GET.get('etiqueta')
        if etiqueta_id:
            queryset = queryset.filter(etiquetas__id=etiqueta_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.get_queryset().filter(completo=False).count()
        context['categorias'] = Categoria.objects.all()
        context['etiquetas'] = Etiqueta.objects.all()
        valor_buscado = self.request.GET.get('area-buscar') or ''
        categoria_id = self.request.GET.get('categoria', None)
        etiqueta_id = self.request.GET.get('etiqueta', None)

        # Convertimos las categorías y etiquetas a enteros si están presentes
        if categoria_id:
            try:
                categoria_id = int(categoria_id)
            except ValueError:
                categoria_id = None
        if etiqueta_id:
            try:
                etiqueta_id = int(etiqueta_id)
            except ValueError:
                etiqueta_id = None

        # Filtro por categoría y etiqueta
        if categoria_id:
            context['tareas'] = context['tareas'].filter(categoria__id=categoria_id)
        if etiqueta_id:
            context['tareas'] = context['tareas'].filter(etiquetas__id=etiqueta_id)

        # Filtro por búsqueda de texto
        if valor_buscado:
            context['tareas'] = context['tareas'].filter(titulo__icontains=valor_buscado)

        context['valor_buscado'] = valor_buscado
        context['categoria_id'] = categoria_id  # Pasamos el id de la categoría al contexto
        context['etiqueta_id'] = etiqueta_id  # Pasamos el id de la etiqueta al contexto

        return context


class Logueo(LoginView):
    template_name = 'base/login.html'
    field = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tareas')


class Registro(FormView):
    template_name = 'base/registro.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tareas')

    def form_valid(self, form):
        usuario = form.save()
        if usuario is not None:
            login(self.request,usuario)
        return super(Registro, self).form_valid(form)

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tareas')
        return super(Registro,self).get(*args,**kwargs)


class DetalleTarea(LoginRequiredMixin, DetailView):
    model = Tarea
    context_object_name = 'tarea'

    def get_queryset(self):
        return super().get_queryset().select_related("usuario")


class CrearTarea(LoginRequiredMixin, CreateView):
    model = Tarea
    form_class = TareaForm
    success_url = reverse_lazy('tareas')

    def form_valid(self, form):
        form.instance.usuario_id = self.request.user.id
        return super().form_valid(form)


class EditarTarea(LoginRequiredMixin, UpdateView):
    model = Tarea
    form_class = TareaForm
    success_url = reverse_lazy('tareas')


class EliminarTarea(LoginRequiredMixin, DeleteView):
    model = Tarea
    context_object_name = 'tarea'
    success_url = reverse_lazy('tareas')


# Vista para crear categoría, solo para administradores
class CrearCategoria(UserPassesTestMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'base/crear_categoria.html'
    success_url = reverse_lazy('categoria-lista')

    def test_func(self):
        return self.request.user.is_superuser

# Vista para crear etiqueta, solo para administradores
class CrearEtiqueta(UserPassesTestMixin, CreateView):
    model = Etiqueta
    form_class = EtiquetaForm
    template_name = 'base/crear_etiqueta.html'
    success_url = reverse_lazy('etiqueta-lista')

    def test_func(self):
        return self.request.user.is_superuser


class ListaCategoria(UserPassesTestMixin,ListView):
    model = Categoria
    context_object_name = 'categorias'
    template_name = 'base/lista_categoria.html'

    def test_func(self):
        return self.request.user.is_superuser


class ListaEtiqueta(UserPassesTestMixin,ListView):
    model = Etiqueta
    context_object_name = 'etiquetas'
    template_name = 'base/lista_etiqueta.html'

    def test_func(self):
        return self.request.user.is_superuser


class EditarCategoria(UserPassesTestMixin,UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'base/crear_categoria.html'
    success_url = reverse_lazy('categoria-lista')

    def test_func(self):
        return self.request.user.is_superuser


class EditarEtiqueta(UserPassesTestMixin,UpdateView):
    model = Etiqueta
    form_class = EtiquetaForm
    template_name = 'base/crear_etiqueta.html'
    success_url = reverse_lazy('etiqueta-lista')

    def test_func(self):
        return self.request.user.is_superuser


class EliminarCategoria(UserPassesTestMixin,DeleteView):
    model = Categoria
    context_object_name = 'categoria'
    template_name = 'base/categoria_confirm_delete.html'
    success_url = reverse_lazy('categoria-lista')


    def test_func(self):
        return self.request.user.is_superuser


class ELiminarEtiqueta(UserPassesTestMixin,DeleteView):
    model = Etiqueta
    context_object_name = 'etiqueta'
    template_name = 'base/etiqueta_confirm_delete.html'
    success_url = reverse_lazy('etiqueta-lista')

    def test_func(self):
        return self.request.user.is_superuser


class ListaUsuarios(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = User
    template_name = 'admin/lista_usuarios.html'
    context_object_name = 'usuarios'

    def test_func(self):
        return self.request.user.is_superuser  # Solo los administradores pueden ver esta vista


# Vista para editar usuarios
class EditarUsuario(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = UsuarioForm
    template_name = 'admin/editar_usuario.html'
    success_url = reverse_lazy('lista-usuarios')

    def test_func(self):
        return self.request.user.is_superuser  # Solo los administradores pueden editar usuarios


# Vista para eliminar usuarios
class EliminarUsuario(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'admin/eliminar_usuario.html'
    success_url = reverse_lazy('lista-usuarios')

    def test_func(self):
        return self.request.user.is_superuser