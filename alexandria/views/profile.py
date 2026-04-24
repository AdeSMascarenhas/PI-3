# Adicione ao seu views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from alexandria.models import Livro, Interesse, Troca

class ProfileView(LoginRequiredMixin, TemplateView):
    """Página de perfil do usuário (requer login)"""
    template_name = "profile.html"
    login_url = 'login'  # Redireciona para login se não estiver autenticado
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Livros do usuário
        context['livros'] = Livro.objects.filter(id_dono=user)
        
        # Interesses do usuário (livros que ele quer)
        context['interesses'] = Interesse.objects.filter(id_usuario=user).select_related('id_livro', 'id_livro__id_dono')
        
        # Trocas realizadas (como dono ou interessado)
        context['trocas'] = Troca.objects.filter(
            models.Q(id_dono=user) | models.Q(id_interessado=user)
        ).select_related('id_livro', 'id_dono', 'id_interessado').order_by('-data_troca')
        
        return context