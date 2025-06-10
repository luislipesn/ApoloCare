from django.db import models

class Nutricionista(models.Model):
    nome = models.CharField(max_length=100)
    crn = models.CharField(max_length=20, unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    dt_nasc = models.DateField
    sexo = models.CharField(max_length=1)
    telefone = models.CharField(max_length=20)
    email = models.CharField(max_length=150)
    

    def __str__(self):
        return self.nome
