# explore.py
from django.views.generic import TemplateView
from django.db.models import Q
from ..models import Livro, Usuario  # Ajuste o caminho do import conforme sua estrutura

class Explore(TemplateView):
    template_name = "explore.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        queryset = Livro.objects.filter(disponivel=True) \
                                .exclude(titulo__isnull=True) \
                                .exclude(titulo__exact='') \
                                .select_related('id_dono')

        # Filtros da URL
        search = self.request.GET.get('search', '').strip()
        regiao = self.request.GET.get('regiao', '')
        estado = self.request.GET.get('estado', '')
        tipo = self.request.GET.get('tipo', '')

        # Busca por título ou autor
        if search:
            queryset = queryset.filter(
                Q(titulo__icontains=search) |
                Q(autor__icontains=search)
            )

        # Região (vem do dono do livro)
        if regiao:
            queryset = queryset.filter(id_dono__regiao=regiao)

        # Estado
        if estado:
            queryset = queryset.filter(estado=estado)

        # Tipo
        if tipo == 'doacao':
            queryset = queryset.filter(em_doacao=True)
        elif tipo == 'troca':
            queryset = queryset.filter(em_doacao=False)

        # Contexto extra pro template
        context['livros'] = queryset
        
        context['filtros'] = {
            'search': search or '',
            'regiao': regiao or '',
            'estado': estado or '',
            'tipo': tipo or '',
        }

        # Regiões 
        context['regioes'] = Usuario._meta.get_field('regiao').choices

        return context