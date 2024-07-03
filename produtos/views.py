from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def logoutUser(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'home.html')


@login_required
def cadastrarproduto(request):
    if request.method == "GET":
        insumos = Insumo.objects.filter(ativo=True)

        return render(request, "cadastrarProduto.html", {"insumos": insumos, "status": 0})
    else:
        nome = request.POST['nome']
        descricao = request.POST['descricao']
        preco = request.POST['preco']
        foto = request.FILES.get('foto')
        insumos_ids = request.POST.getlist('insumo[]')
        quantidades = request.POST.getlist('quantidade[]')
        if foto:
            produto= Produto(nome=nome,descricao=descricao,preco_unitario= preco,imagem=foto)
        else:
            produto= Produto(nome=nome,descricao=descricao,preco_unitario= preco)
        produto.save()
        for insumoid,quantidade in zip(insumos_ids,quantidades):
            if insumoid and insumoid !=" ":
                insumo=Insumo.objects.get(id=insumoid)
                insumoproduto=InsumoProduto(insumo=insumo,produto=produto,quantidade=quantidade)
                insumoproduto.save()
        
        
    return redirect('home')
@login_required
def lista_produtos(request):
    produtos=(Produto.objects.filter(ativo=1))
    for produto in produtos:
        produto.custo=produto.calcula_preco() 
        produto.lucro=produto.preco_unitario-produto.custo
    return render(request, 'lista_custo_produtos.html',{'produtos':produtos})
