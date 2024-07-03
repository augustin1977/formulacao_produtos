from django.db import models


class Insumo(models.Model):
    nome = models.CharField(max_length=255)
    preco_unitario = models.DecimalField(max_digits=11,decimal_places=2)
    ativo=models.BooleanField(default=True)
    def __str__(self):
        return f"{self.nome}"
class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao= models.TextField()
    preco_unitario = models.DecimalField(max_digits=11,decimal_places=2)
    imagem=models.FileField(null=True,blank=True,upload_to='media')
    data_atualização=models.DateTimeField(auto_now=True)
    ativo=models.BooleanField(default=True)
    def calcula_preco(self):
        insumosprodutos=InsumoProduto.objects.filter(ativo=1).filter(produto=self)
        custo=0
        for insumoproduto in insumosprodutos:
             custo+=insumoproduto.insumo.preco_unitario*insumoproduto.quantidade
        return custo
            
    def __str__(self):
        return f"{self.nome}"
              
class InsumoProduto(models.Model):
    insumo=models.ForeignKey(Insumo, on_delete=models.CASCADE)
    produto=models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=15,decimal_places=4)
    ativo=models.BooleanField(default=True)
    def __str__(self):
            return f"{self.produto} utiliza {self.quantidade} de {self.insumo}"

