from sistema import app, db, mapeamento_breadcrumbs, redirect, request, render_template, flash, url_for, get_page_args, Pagination, current_user
from sistema.models.base_model import datetime
from sistema.models.almoxarifado_model import Almoxarifado
from sistema.models.categoria_produto_model import CategoriaProduto
from sistema.models.produto_movimentacoes_model import ProdutoMovimentacoes
from sistema import or_, desc
from sistema.utils.formata_valor import formatacao_valor_numerico
from sistema.utils.formata_data import formatar_data_brasil

import locale
"""

CRUD almoxarifado

"""


@app.route('/almoxarifado',  methods=['GET', 'POST'])
def almoxarifado():
    search_query = request.args.get('search')
    # Setando variáveis da página atual (1), quantidade de itens por página (10)
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    produtos_query = Almoxarifado.query.filter_by(
        ativo=True)
    categoria_filter = request.args.get('categoria-produto')
    total = produtos_query.count()
    categoria_produtos = CategoriaProduto.query.all()

    if search_query:
        produtos_query = produtos_query.filter(or_(
            Almoxarifado.codigo_produto.ilike(f'%{search_query}%'),
            Almoxarifado.nome.ilike(f'%{search_query}%'),
            Almoxarifado.valor.ilike(f'%{search_query}%'),
        ))

    if categoria_filter:
        produtos_query = produtos_query.filter(
            Almoxarifado.categoria_produto_id == categoria_filter)

    # Ordenação baseada nos parâmetros recebidos
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction', 'asc')

    if order_by:
        if order_direction == 'asc':
            # Caso a ordenação seja por ordem crescente:
            if order_by == 'codigo_produto':
                produtos_query = produtos_query.order_by(
                    Almoxarifado.codigo_produto.asc())

            elif order_by == 'nome':
                produtos_query = produtos_query.order_by(
                    Almoxarifado.nome.asc())

            elif order_by == 'valor':
                produtos_query = produtos_query.order_by(
                    Almoxarifado.valor.asc())

            elif order_by == 'quantidade_estoque':
                produtos_query = produtos_query.order_by(
                    Almoxarifado.quantidade_estoque.asc())

        elif order_direction == 'desc':
            # Caso a ordenação seja por ordem decrescente:
            if order_by == 'codigo_produto':
                produtos_query = produtos_query.order_by(
                    Almoxarifado.codigo_produto.desc())

            elif order_by == 'nome':
                produtos_query = produtos_query.order_by(
                    Almoxarifado.nome.desc())

            elif order_by == 'valor':
                produtos_query = produtos_query.order_by(
                    Almoxarifado.valor.desc())

            elif order_by == 'quantidade_estoque':
                produtos_query = produtos_query.order_by(
                    Almoxarifado.quantidade_estoque.desc())

    # Tratamento para mudança de direção de ordenação ao usuário clicar novamente na tag (caso for 'desc', virará 'asc' e vice-versa)
    next_order_direction = 'asc' if order_direction == 'desc' else 'desc'

    # Atualizando a totalidade de produtos (contador)
    total = produtos_query.count()
    # Setando novamente a ordenação pela data_criacao
    produtos_query = produtos_query.order_by(desc(Almoxarifado.data_criacao))
    produtos = produtos_query.offset(offset).limit(per_page).all()
    pagination = Pagination(page=page, offset=offset,
                            per_page=per_page, total=total, css_framework='bootstrap')
    # Incrementando as páginas para ir para a próxima página
    next_page = pagination.page + 1
    # Decrementando as páginas para voltar uma página
    prev_page = pagination.page - 1

    return render_template('pages-almoxarifado/listagem-produtos.html', categoria_produtos=categoria_produtos,
                           formatacao_valor_numerico=formatacao_valor_numerico,
                           pagination=pagination,
                           next_page=next_page,
                           prev_page=prev_page,
                           order_by=order_by,
                           order_direction=order_direction,
                           next_order_direction=next_order_direction,
                           produtos=produtos,
                           mapeamento_breadcrumbs=mapeamento_breadcrumbs)


@app.route('/almoxarifado/criar_produto', methods=['GET', 'POST'])
def criarProduto():
    categorias_produtos = CategoriaProduto.query.all()

    if request.method == 'POST':
        nome = request.form['produto-nome']
        codigo_produto = request.form['produto-codigo']
        codigo_barras = request.form['produto-codigo-barras']
        categoria_produto = request.form['produto-categoria']
        # Substituindo o separador decimal ',' por '.'
        valor = float(request.form['produto-valor'].replace(',', '.'))
        estoque = float(request.form['produto-estoque'].replace(',', '.'))
        valor_total = valor * estoque

        # Verificação para ver se o nome, codigo de produto e barras já está cadastrado no banco
        produto_existe = Almoxarifado.query.filter_by(nome=nome).first()
        codigo_existe = Almoxarifado.query.filter_by(
            codigo_produto=codigo_produto).first()
        codigo_barras_existe = Almoxarifado.query.filter_by(
            codigo_barras=codigo_barras).first()

        if produto_existe or codigo_existe or codigo_barras_existe:
            flash(
                'O produto que você está tentando cadastrar já existe. Tente novamente.', 'danger')
            return redirect(url_for('criarProduto'))

        if categoria_produto == 0 or categoria_produto == '0':
            flash(
                'A categoria de produto não foi informada. Informe uma categoria.', 'danger')
        else:
            # Condição para caso o usuário digite um produto em minúsculo
            if nome.islower():
                # Transformando a primeira letra com CAPS LOCK
                nome = nome.capitalize()

            # Condição para caso o usuário digite um produto em letra maiúscula
            elif nome.isupper():
                nome = nome.capitalize()

            # Salvando informações no banco
            produto = Almoxarifado(
                nome, codigo_produto, codigo_barras, categoria_produto, valor, estoque, valor_total)
            
            db.session.add(produto)
            db.session.commit()

            #Atribuindo o nome do usuário atual como responsável
            responsavel = current_user.nome
            # Cálculo da diferença entre o estoque recebido pelo form e o já existente
            quantidade_movimentada = estoque - produto.quantidade_estoque
            # Setando como entrada, pois é o caddastro
            tipo = 'Entrada'
            # Criando uma nova movimentação
            movimentacao = ProdutoMovimentacoes(
                responsavel=responsavel,
                tipo=tipo,
                quantidade_movimentada=abs(quantidade_movimentada),
                quantidade_estoque=estoque,
                valor_unitario=valor,
                valor_total=valor_total,
                produto_id=produto.id
            )
            #Salvando a movimentação inicial (cadastro)
            db.session.add(movimentacao)
            db.session.commit()

            if produto:
                flash('Produto cadastrado! ', 'success')
                return redirect(url_for('almoxarifado'))

    return render_template('pages-almoxarifado/criar_produto.html', mapeamento_breadcrumbs=mapeamento_breadcrumbs,
                           categorias_produtos=categorias_produtos)


@app.route('/almoxarifado/visualizar/produto/<int:id>', methods=['GET', 'POST'])
def visualizarProduto(id):
    produto = Almoxarifado.query.get(id)
    categoria_produto = CategoriaProduto.query.get(
        produto.categoria_produto_id)

    return render_template('/pages-almoxarifado/visualizar_produto.html', categoria_produto=categoria_produto,
                           formatacao_valor_numerico=formatacao_valor_numerico,
                           produto=produto,
                           mapeamento_breadcrumbs=mapeamento_breadcrumbs)


@app.route('/almoxarifado/editar/produto/<int:id>', methods=['GET', 'POST'])
def editarProduto(id):
    produto = Almoxarifado.query.get(id)
    categorias_produtos = CategoriaProduto.query.all()

    if produto:
        categoria_produto = CategoriaProduto.query.get(
            produto.categoria_produto_id)

        if request.method == 'POST':
            nome = request.form['produto-nome']
            codigo_produto = request.form['produto-codigo']
            codigo_barras = request.form['produto-codigo-barra']
            categoria_produto_id = request.form['produto-categoria']
            # Pegando o valor em string do form
            valor = request.form['produto-valor']
            estoque = request.form['produto-estoque']
            # Substituindo '.' em branco e substituindo ',' por '.'
            valor = valor.replace('.', '').replace(',', '.')
            estoque = estoque.replace('.', '').replace(',', '.')

            valor_total = float(valor) * float(estoque)

            #Atribuindo o nome do usuário atual como responsável
            responsavel = current_user.nome
            # Cálculo da diferença entre o estoque recebido pelo form e o já existente
            quantidade_movimentada = float(estoque) - produto.quantidade_estoque
            
            if quantidade_movimentada != 0:
                tipo = 'Entrada' if quantidade_movimentada > 0 else 'Saída'
                # Criando uma nova movimentação
                movimentacao = ProdutoMovimentacoes(
                    responsavel=responsavel,
                    tipo=tipo,
                    quantidade_movimentada=abs(quantidade_movimentada),
                    quantidade_estoque=estoque,
                    valor_unitario=valor,
                    valor_total=valor_total,
                    produto_id=id
                )

                db.session.add(movimentacao)

            # Referenciando colunas que serão atualizadas
            produto.nome = nome
            produto.codigo_produto = codigo_produto
            produto.codigo_barras = codigo_barras

            categoria_produto = CategoriaProduto.query.get(categoria_produto_id)

            if categoria_produto:
                produto.categoria_produto_id = categoria_produto_id
            else:
                flash('Categoria de produto inválida.', 'danger')
                return redirect(url_for('editarProduto', id=id))

            produto.valor = valor
            produto.quantidade_estoque = estoque
            produto.valor_total = valor_total

            # Salvando no DB e mandando informação ao usuário
            db.session.commit()
            flash('Produto editado com sucesso.', 'success')
            return redirect(url_for('almoxarifado'))

    return render_template('/pages-almoxarifado/editar_produto.html', produto=produto,
                           formatacao_valor_numerico=formatacao_valor_numerico,
                           categorias_produtos=categorias_produtos,
                           categoria_produto=categoria_produto,
                           mapeamento_breadcrumbs=mapeamento_breadcrumbs)



@app.route('/almoxarifado/excluir/produto/<int:id>', methods=['GET', 'POST'])
def excluirProduto(id):
    produto = Almoxarifado.query.get(id)

    if request.method == 'POST':
        if produto:
            produto.ativo = False
            db.session.commit()
            flash('Produto removido com sucesso!', 'success')
            return redirect(url_for('almoxarifado'))


"""
Páginas Movimentações de Estoque dos Produtos

"""

@app.route('/almoxarifado/produtos/<int:id>/movimentacoes', methods=['GET', 'POST'])
def listagemMovimentacoes(id):
    produto = Almoxarifado.query.get(id)

    total_entrada, total_saida = produto.total_movimentacoes

    movimentacoes = ProdutoMovimentacoes.query.filter_by(produto_id=id).order_by(desc(ProdutoMovimentacoes.data_criacao)).all()



    return render_template('/pages-almoxarifado/produtos_movimentacoes.html', produto=produto, 
                           movimentacoes=movimentacoes,
                           formatacao_valor_numerico=formatacao_valor_numerico,
                           formatar_data_brasil=formatar_data_brasil,
                           total_entrada=total_entrada,
                           total_saida=total_saida,
                           mapeamento_breadcrumbs=mapeamento_breadcrumbs)

"""

CRUD categoria_produto

"""


@app.route('/almoxarifado/criar_categoria_produto', methods=['GET', 'POST'])
def criarCategoriaProduto():
    if request.method == 'POST':
        tipo = request.form['produto-categoria']

        categoria_existe = CategoriaProduto.query.filter_by(tipo=tipo).first()

        if categoria_existe:
            flash(
                'A categoria que você está tentando cadastrar já existe. Tente outra. ', 'danger')

        else:
            if tipo.islower():
                # Transformando a primeira letra com CAPS LOCK
                tipo = tipo.capitalize()

            # Condição para caso o usuário digite uma categoria em letra maiúscula
            elif tipo.isupper():
                tipo = tipo.capitalize()

            categoria_produto = CategoriaProduto(tipo)

            db.session.add(categoria_produto)
            db.session.commit()

            if categoria_produto:
                flash('Categoria do produto cadastrada!', 'success')

        categorias_produtos = CategoriaProduto.query.all()

    return render_template('pages-almoxarifado/criar_produto.html', mapeamento_breadcrumbs=mapeamento_breadcrumbs,
                           categorias_produtos=categorias_produtos)


@app.route('/almoxarifado/editar_categoria_produto/<int:id>', methods=['POST'])
def editarCategoriaProduto(id):
    categoria_produto = CategoriaProduto.query.get(id)

    if categoria_produto:
        if request.method == 'POST':
            tipo = request.form['produto-categoria']
            categoria_produto.tipo = tipo
            db.session.commit()
            flash('Categoria do produto editada com sucesso!', 'success')

        # Redireciona ao produto associado a categoria
        produto = Almoxarifado.query.filter_by(categoria_produto_id=id).first()

        if produto:
            return redirect(url_for('editarProduto', id=produto.id))

    flash('Categoria do produto não encontrada.', 'danger')
    return redirect(url_for('almoxarifado'))


@app.route('/almoxarifado/excluir_categoria_produto/<int:id>', methods=['POST'])
def excluirCategoriaProduto(id):
    categoria_produto = CategoriaProduto.query.get(id)

    if categoria_produto:
        categoria_produto.ativo = False
        db.session.commit()
        flash('Categoria removida com sucesso!', 'success')

        produto = Almoxarifado.query.filter_by(categoria_produto_id=id).first()

        if produto:
            return redirect(url_for('editarProduto', id=produto.id))
        else:
            return redirect(url_for('almoxarifado'))

    flash('Categoria não encontrada!', 'error')
    return redirect(url_for('almoxarifado'))
