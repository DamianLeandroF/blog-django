from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import PostForm
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.select_related('autor')
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(Q(titulo__icontains=q) | Q(contenido__icontains=q))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '').strip()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        messages.success(self.request, 'Post creado correctamente.')
        return super().form_valid(form)


class AutorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().autor == self.request.user


class PostUpdateView(LoginRequiredMixin, AutorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Post actualizado correctamente.')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, AutorRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:list')

    def form_valid(self, form):
        messages.success(self.request, 'Post eliminado correctamente.')
        return super().form_valid(form)
