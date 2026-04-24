# explore.py
from django.views.generic import TemplateView
from ..models import Livro  # Ajuste o caminho do import conforme sua estrutura

class Explore(TemplateView):
    template_name = "explore.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        livros = Livro.objects.filter(disponivel=True).exclude(titulo__isnull=True)
        context['livros'] = livros
        return context