from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, password=None, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, password=None, **extra_fields):
        extra_fields.setdefault('administrador', True)
        extra_fields.setdefault('moderador', True)
        extra_fields.setdefault('ativo', True)
        return self.create_user(email, nome, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    """
    Modelo customizado sem username, usando e-mail como login.
    Permissões baseadas nos campos moderador, administrador e ativo.
    """
    id = models.AutoField(primary_key=True)
    # Campos da tabela original
    nome = models.CharField(max_length=256, verbose_name='Nome completo do usuário')
    email = models.EmailField(max_length=256, unique=True, verbose_name='E‑mail único por usuário')
    regiao = models.CharField(
        max_length=30,
        choices=[
            ('NORTE 1', 'NORTE 1'),
            ('NORTE 2', 'NORTE 2'),
            ('LESTE 1', 'LESTE 1'),
            ('LESTE 2', 'LESTE 2'),
            ('SUL', 'SUL'),
            ('SUDESTE', 'SUDESTE'),
            ('SUDOESTE', 'SUDOESTE'),
            ('OESTE', 'OESTE'),
            ('CENTRO', 'CENTRO'),
            ('REGIAO METROPOLITANA', 'REGIAO METROPOLITANA'),
        ],  # suas escolhas
        verbose_name='Região'
    )
    cidade = models.CharField(max_length=50, default='São Paulo')
    password = models.CharField(max_length=128, db_column='senha', verbose_name='Senha')

    # Seus campos booleanos personalizados
    moderador = models.BooleanField(db_column='moderador', default=False)
    administrador = models.BooleanField(db_column='administrador', default=False)
    ativo = models.BooleanField(db_column='ativo', default=True)

    # Remove campos desnecessários do AbstractBaseUser/PermissionsMixin
    # Mas PermissionsMixin exige is_superuser, is_staff, is_active – vamos sobrescrever como propriedades
    # Para evitar colunas extras, usamos properties que leem nossos campos.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    objects = UsuarioManager()

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuário'

    def __str__(self):
        return self.nome

    # Propriedades exigidas pelo Django (mas redirecionam para nossos campos)
    @property
    def is_staff(self):
        """Usuário com `administrador` ou `moderador` pode acessar o admin."""
        return self.administrador or self.moderador

    @property
    def is_superuser(self):
        """Usuário com `administrador` é considerado superusuário."""
        return self.administrador

    @property
    def is_active(self):
        """Usa o campo `ativo` para desativar login."""
        return self.ativo

    # Permissões personalizadas (opcional)
    def has_perm(self, perm, obj=None):
        # Se for administrador, tem todas as permissões
        if self.administrador:
            return True
        # Se for moderador, pode ter permissões específicas (ex: moderar livros)
        # Implemente conforme sua lógica
        return False

    def has_module_perms(self, app_label):
        return self.administrador or self.moderador

class Livro(models.Model):
    ESTADO_CHOICES = [
        ('OTIMO', 'Ótimo'),
        ('BOM', 'Bom'),
        ('NORMAL', 'Normal'),
        ('DANIFICADO', 'Danificado'),
    ]

    id = models.AutoField(primary_key=True, verbose_name='Identificador único do livro')
    id_dono = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        db_column='id_dono',  # nome exato da coluna no banco
        verbose_name='Dono do livro'
    )
    cod_api = models.IntegerField(null=True, blank=True, verbose_name='Código de integração com API externa')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, verbose_name='Estado de conservação do livro')
    disponivel = models.BooleanField(default=True, verbose_name='Disponível para troca/empréstimo')
    em_doacao = models.BooleanField(default=False, verbose_name='Disponível para doação')

    class Meta:
        db_table = 'livros'
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'

    def __str__(self):
        return f'Livro {self.id} - Dono: {self.id_dono.nome}'


class Interesse(models.Model):
    id_usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        db_column='id_usuario',
        verbose_name='Usuário interessado'
    )
    id_livro = models.ForeignKey(
        Livro, 
        on_delete=models.CASCADE, 
        db_column='id_livro',
        verbose_name='Livro de interesse'
    )
    data_interesse = models.DateTimeField(default=timezone.now, verbose_name='Quando o interesse foi registrado')

    class Meta:
        db_table = 'interesses'
        constraints = [
            models.UniqueConstraint(fields=['id_usuario', 'id_livro'], name='unique_interesse')
        ]
        verbose_name = 'Interesse'
        verbose_name_plural = 'Interesses'

    def __str__(self):
        return f'{self.id_usuario.nome} interessado em {self.id_livro.id}'


class Troca(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='Identificador único da troca')
    id_dono = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='trocas_como_dono',
        db_column='id_dono',
        verbose_name='Dono do livro'
    )
    id_interessado = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='trocas_como_interessado',
        db_column='id_interessado',
        verbose_name='Interessado no livro'
    )
    id_livro = models.ForeignKey(
        Livro, 
        on_delete=models.CASCADE, 
        db_column='id_livro',
        verbose_name='Livro em transação'
    )
    data_troca = models.DateField(default=timezone.now, verbose_name='Data da troca')

    class Meta:
        db_table = 'troca'
        verbose_name = 'Troca'
        verbose_name_plural = 'Trocas'

    def __str__(self):
        return f'Troca {self.id} - Livro {self.id_livro.id}'