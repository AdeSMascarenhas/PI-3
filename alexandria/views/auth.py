# views.py ou auth.py
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from alexandria.models import Usuario

class LoginView(TemplateView):
    """Página única com login à esquerda e cadastro à direita"""
    template_name = "login.html"
    
    def dispatch(self, request, *args, **kwargs):
        # Se o usuário já está logado, redireciona para a home
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adiciona o next se existir
        context['next'] = self.request.GET.get('next', 'home')
        return context

class SigninView(TemplateView):
    """Página única com login à esquerda e cadastro à direita"""
    template_name = "signin.html"
    
    def dispatch(self, request, *args, **kwargs):
        # Se o usuário já está logado, redireciona para a home
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adiciona o next se existir
        context['next'] = self.request.GET.get('next', 'home')
        return context


class LogoutView(TemplateView):
    """Processa o logout"""
    http_method_names = ['get']
    
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, 'Até logo, espero que nos encontremos bem na próxima.')
        return redirect('login')

class ProcessLogin(TemplateView):
    """Processa o login via POST"""
    http_method_names = ['post']
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        next_url = request.POST.get('next', 'home')
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo(a) de volta, {user.nome}!')
            return redirect('login')
        else:
            messages.error(request, 'E-mail ou senha inválidos.')
            return redirect('login')


class ProcessSignin(TemplateView):
    """Processa o cadastro via POST"""
    http_method_names = ['post']
    
    def post(self, request, *args, **kwargs):
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        regiao = request.POST.get('regiao')
        cidade = request.POST.get('cidade', 'São Paulo')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validações
        if password != password_confirm:
            messages.error(request, 'As senhas não coincidem.')
            return redirect('signin')
        
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
            return redirect('signin')
        
        if not regiao:
            messages.error(request, 'Selecione uma região.')
            return redirect('signin')
        
        # Cria o usuário
        user = Usuario.objects.create_user(
            email=email,
            nome=nome,
            password=password
        )
        user.regiao = regiao
        user.cidade = cidade
        user.save()
        
        # Autentica e loga automaticamente
        user_authenticated = authenticate(request, email=email, password=password)
        if user_authenticated:
            login(request, user_authenticated)
            messages.success(request, f'Cadastro realizado com sucesso! Bem-vindo(a), {nome}!')
            return redirect('home')
        
        return redirect('signin')

