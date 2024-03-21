from sistema import app, db, render_template, redirect, url_for, flash, request, mapeamento_breadcrumbs, get_page_args, Pagination
from sistema.models.imovel_model import Imovel
from sistema.models.observacao_model import Observacao
from sistema import or_, desc
from sistema.utils.formata_data import formatar_data_brasil


@app.route('/observacoes', methods=['GET', 'POST'])
def observacoes():
    imoveis = Imovel.query.all()
    observacoes_query = Observacao.query.filter_by(ativo=True).order_by(desc(Observacao.data_criacao))

    search_query = request.args.get('search')

    if search_query:
        observacoes_query = observacoes_query.filter(or_(
            Observacao.descricao.ilike(f'%{search_query}%')
        ))

    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')

    # Atualizando a totalidade de imoveis (contador)
    total = observacoes_query.count()

    pagination = Pagination(page=page, per_page=per_page,
                            total=total, css_framework='bootstrap')

    # Verificando se a página solicitada está dentro do intervalo válido
    if page < 1 or page > len(list(pagination.pages)):
        page = 1

    # Recuperando as observações da página atual
    observacoes = observacoes_query.offset(
        (page - 1) * per_page).limit(per_page).all()

    # Verificando páginas anteriores e posteriores
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < len(list(pagination.pages)) else None

    return render_template('pages-observacoes/listagem-observacoes.html',
                           mapeamento_breadcrumbs=mapeamento_breadcrumbs,
                           imoveis=imoveis,
                           formatar_data_brasil=formatar_data_brasil,
                           next_page=next_page,
                           prev_page=prev_page,
                           pagination=pagination,
                           observacoes=observacoes)


@app.route('/observacoes/criar_observacao', methods=['GET', 'POST'])
def criarObservacao():
    imoveis = Imovel.query.all()
    observacoes = Observacao.query.all()

    if request.method == 'POST':
        descricao = request.form['observacaoDescricao']
        possui_imovel_vinculado = request.form['possui_imovel_vinculado']
        possui_imovel_vinculado_boolean = eval(possui_imovel_vinculado)
        imovel_id = request.args.get('imovel_disponivel')
        
        try:
            observacao = Observacao(
                descricao=descricao, possui_imovel_vinculado=possui_imovel_vinculado_boolean, imovel_id=imovel_id)
            db.session.add(observacao)
            db.session.commit()
            flash('Observação cadastrada com sucesso!', 'success')
            return redirect(url_for('observacoes'))

        except:
            flash('Erro ao cadastrar a observação.', 'warning')

    return render_template('pages-observacoes/criar-observacao.html',
                           mapeamento_breadcrumbs=mapeamento_breadcrumbs,
                           imoveis=imoveis,
                           observacoes=observacoes)


@app.route('/observacoes/editar_observacao/<int:id>', methods=['GET', 'POST'])
def editarObservacao(id):
    imoveis = Imovel.query.all()
    observacoes = Observacao.query.all()
    observacao = Observacao.query.get(id)

    if request.method == 'POST':
        descricao = request.form['observacaoDescricao']
        possui_imovel_vinculado = request.form.get('possui_imovel_vinculado')
        possui_imovel_vinculado_boolean = eval(possui_imovel_vinculado)
        imovel_id = request.form.get('imovel_disponivel')

        # Setando informações recebidas
        observacao.descricao = descricao
        observacao.possui_imovel_vinculado = possui_imovel_vinculado_boolean

        if possui_imovel_vinculado_boolean == 1:
            observacao.imovel_id = imovel_id
        else:
            observacao.imovel_id = None

        db.session.commit()
        flash('Observação editada com sucesso!', 'success')
        return redirect(url_for('observacoes'))

    return render_template('pages-observacoes/editar-observacao.html',
                           mapeamento_breadcrumbs=mapeamento_breadcrumbs,
                           observacao=observacao,
                           imoveis=imoveis,
                           observacoes=observacoes)


@app.route('/observacoes/excluir_observacao/<int:id>', methods=['GET', 'POST'])
def excluirObservacao(id):
    observacao = Observacao.query.get(id)

    if request.method == 'POST':
        if observacao:
            observacao.ativo = False
            observacao.imovel_id = None
            db.session.commit()
            flash('Observação removida com sucesso!', 'success')
            return redirect(url_for('observacoes'))
