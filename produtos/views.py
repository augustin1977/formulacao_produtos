from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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

@login_required
def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    insumos = Insumo.objects.all()

    if request.method == 'POST':
        produto.nome = request.POST.get('nome')
        produto.descricao = request.POST.get('descricao')
        produto.preco = request.POST.get('preco')
        if 'foto' in request.FILES:
            produto.foto = request.FILES['foto']
        produto.save()

        # Remove todos os insumos existentes para o produto
        produto.insumos.clear()

        # Adiciona os novos insumos
        insumo_ids = request.POST.getlist('insumo[]')
        quantidades = request.POST.getlist('quantidade[]')
        for insumo_id, quantidade in zip(insumo_ids, quantidades):
            if insumo_id:
                insumo = get_object_or_404(Insumo, id=insumo_id)
                produto.insumos.add(insumo, through_defaults={'quantidade': quantidade})

        messages.success(request, 'Produto atualizado com sucesso!')
        return redirect('listarprodutos')

    # Obtenha os insumos associados ao produto
    produto_insumos = InsumoProduto.objects.filter(produto=produto)
    print(produto_insumos)
    return render(request, 'editar_produto.html', {
        'produto': produto,
        'insumos': insumos,
        'produto_insumos': produto_insumos
    })