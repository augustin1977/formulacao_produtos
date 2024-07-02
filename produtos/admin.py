from django.contrib import admin


from .models import Produto,Insumo,InsumoProduto

admin.site.register(Produto)
admin.site.register(Insumo)
admin.site.register(InsumoProduto)