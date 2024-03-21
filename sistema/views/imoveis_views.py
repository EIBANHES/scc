from sistema import app, db, render_template, redirect, url_for, flash, request, mapeamento_breadcrumbs, get_page_args, Pagination
from sistema.models.imovel_model import Imovel
from sistema.models.pessoa_model import Pessoa
from sistema.models.andar_model import Andar
from sistema.models.tipo_garagem_model import TipoGaragem
from sistema.models.tipo_animal_model import TipoAnimal
from sistema.models.observacao_model import Observacao
from sistema import or_, desc
from sistema.utils.formata_data import formatar_data_brasil

"""

CRUD imoveis

"""


@app.route('/imoveis', methods=['GET', 'POST'])
def imoveis():
    proprietarios = Pessoa.query.all()
    andares = Andar.query.all()
    # Setando variáveis da página atual (1), quantidade de itens por página (10)
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    search_query = request.args.get('search')
    andar_filter = request.args.get('andar')
    apartamento_filter = request.args.get('apartamento')
    imovel_query = Imovel.query.filter_by(
        ativo=True).join(Pessoa.imoveis).join(Andar)
    total = imovel_query.count()

    if search_query:
        imovel_query = imovel_query.filter(or_(
            Andar.nome.ilike(f'%{search_query}%'),
            Imovel.apartamento.ilike(f'%{search_query}%'),
            Pessoa.nome.ilike(f'%{search_query}%'),
        ))

    if andar_filter:
        imovel_query = imovel_query.filter(Andar.id == andar_filter)

    if apartamento_filter:
        imovel_query = imovel_query.filter(
            Imovel.apartamento.ilike(f'%{apartamento_filter}%'))

    # Ordenação baseada nos parâmetros recebidos
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction', 'asc')

    if order_by:
        if order_direction == 'asc':
            # Caso a ordenação seja por ordem crescente:
            if order_by == 'andar':
                imovel_query = imovel_query.order_by(Andar.nome.asc())

            elif order_by == 'apartamento':
                imovel_query = imovel_query.order_by(Imovel.apartamento.asc())

            elif order_by == 'proprietario':
                imovel_query = imovel_query.order_by(Pessoa.nome.asc())

            elif order_by == 'data_criacao':
                imovel_query = imovel_query.order_by(Imovel.data_criacao.asc())

        elif order_direction == 'desc':
            # Caso a ordenação seja por ordem decrescente:
            if order_by == 'andar':
                imovel_query = imovel_query.order_by(Andar.nome.desc())

            elif order_by == 'apartamento':
                imovel_query = imovel_query.order_by(Imovel.apartamento.desc())

            elif order_by == 'proprietario':
                imovel_query = imovel_query.order_by(Pessoa.nome.desc())

            elif order_by == 'data_criacao':
                imovel_query = imovel_query.order_by(
                    Imovel.data_criacao.desc())

    # Tratamento para mudança de direção de ordenação ao usuário clicar novamente na tag (caso for 'desc', virará 'asc' e vice-versa)
    next_order_direction = 'asc' if order_direction == 'desc' else 'desc'

    # Atualizando a totalidade de imoveis (contador)
    total = imovel_query.count()
    # Setando novamente a ordenação pela data_criacao
    imovel_query = imovel_query.order_by(desc(Imovel.data_criacao))
    imoveis = imovel_query.offset(offset).limit(per_page).all()

    pagination = Pagination(page=page, offset=offset,
                            per_page=per_page, total=total, css_framework='bootstrap')

    # Incrementando as páginas para ir para a próxima página
    next_page = pagination.page + 1
    # Decrementando as páginas para voltar uma página
    prev_page = pagination.page - 1

    return render_template('pages-imoveis/listagem-imoveis.html',
                           proprietarios=proprietarios,
                           imoveis=imoveis,
                           next_page=next_page,
                           prev_page=prev_page,
                           formatar_data_brasil=formatar_data_brasil,
                           andares=andares,
                           pagination=pagination,
                           order_by=order_by,
                           order_direction=order_direction,
                           next_order_direction=next_order_direction,
                           mapeamento_breadcrumbs=mapeamento_breadcrumbs)


@app.route('/imoveis/cadastrar_imovel', methods=['GET', 'POST'])
def cadastrarImovel():
    proprietarios = Pessoa.query.filter(Pessoa.tipo_morador_id.is_(None)).all()
    andares = Andar.query.all()
    andares_garagem = TipoGaragem.query.all()
    categoria_animal = TipoAnimal.query.all()

    if request.method == 'POST':
        andar_selecionado = request.form.get('imovelAndar')
        apartamento = request.form.get('imovelApartamento')
        proprietario = request.form.get('imovelProprietario')
        numero_garagem = request.form.get('imovelNumeroGaragem')
        andar_garagem_selecionado = request.form.get('imovelAndarGaragem')
        possui_pet = request.form.get('possui_pet')
        possui_pet_booleano = eval(possui_pet)
        tipo_animal = request.form.get('tipo_pet')


        # Verificando se o andar cadastrado é igual ao recebido do input do usuário
        andar = Andar.query.get(andar_selecionado)
        andar_garagem = TipoGaragem.query.get(andar_garagem_selecionado)

        # Caso o andar não condiza com o ID da table
        if not andar:
            flash('Por favor, selecione um andar válido. ', 'danger')
            return redirect(url_for('cadastrarImovel'))

        if andar and apartamento and proprietario != '0':
            try:
                imovel = Imovel(
                    andar_id=andar.id, apartamento=apartamento, pessoa_id=proprietario, possui_pet=possui_pet_booleano, 
                    tipo_animal_id=tipo_animal, andar_garagem=andar_garagem.id, numero_garagem=numero_garagem)
                db.session.add(imovel)
                db.session.commit()
                flash('Imóvel cadastrado com sucesso!', 'success')
                return redirect(url_for('listaProprietarios'))
            except:
                flash('Erro ao cadastrar imóvel ao proprietário.', 'warning')
        else:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return redirect(url_for('cadastrarImovel'))

    return render_template('pages-imoveis/cadastrar_imovel.html', andares=andares,
                           andares_garagem=andares_garagem,
                           proprietarios=proprietarios,
                           categoria_animal=categoria_animal,
                           mapeamento_breadcrumbs=mapeamento_breadcrumbs)


@app.route('/imoveis/visualizar/imovel/<int:id>', methods=['GET', 'POST'])
def visualizarImovel(id):
    imovel = Imovel.query.get(id)
    proprietario = Pessoa.query.get(imovel.pessoa_id)
    andar_garagem = TipoGaragem.query.get(imovel.andar_garagem)
    observacoes = Observacao.query.filter_by(imovel_id=id).all()
    observacao = Observacao.query.filter_by(imovel_id=id).first()

    return render_template('pages-imoveis/visualizar_imovel.html',
                           imovel=imovel,
                           proprietario=proprietario,
                           andar_garagem=andar_garagem,
                           observacoes=observacoes,
                           observacao=observacao,
                           mapeamento_breadcrumbs=mapeamento_breadcrumbs)


@app.route('/imoveis/editar/imovel/<int:id>', methods=['GET', 'POST'])
def editarImovel(id):
    imovel = Imovel.query.get(id)
    proprietario = Pessoa.query.get(imovel.pessoa_id)
    proprietarios = Pessoa.query.filter(Pessoa.tipo_morador_id.is_(None)).all()
    categoria_animal = TipoAnimal.query.all()
    andares = Andar.query.all()
    andares_garagem = TipoGaragem.query.all()
    andar_garagem = TipoGaragem.query.get(imovel.andar_garagem)

    if request.method == 'POST':
        andar_selecionado = request.form['imovel-andar']
        apartamento = request.form['imovel-apartamento']
        proprietario_imovel = request.form['imovel-proprietario']
        numero_garagem = request.form['imovel-numero-garagem']
        andar_garagem = request.form['imovel-andar-garagem']
        possui_pet = request.form['possui_pet']
        tipo_animal_id = request.form.get('tipo_pet')
        possui_pet_boolean = eval(possui_pet)

        #Setando informações recebidas
        imovel.andar_id = andar_selecionado
        imovel.apartamento = apartamento
        imovel.possui_pet = possui_pet_boolean
        imovel.tipo_animal_id = tipo_animal_id
        imovel.pessoa_id = proprietario_imovel
        imovel.numero_garagem = numero_garagem
        imovel.andar_garagem = andar_garagem

        if possui_pet_boolean == 0:
            imovel.tipo_animal_id = None
            db.session.commit()
            flash('Imóvel editado com sucesso!', 'success')
            return redirect(url_for('imoveis'))
        else:
            flash('Imóvel editado com sucesso!', 'success')
            db.session.commit()
            return redirect(url_for('imoveis'))

    return render_template('pages-imoveis/editar_imovel.html', imovel=imovel,
                           andares=andares,
                           andar_garagem=andar_garagem,
                           andares_garagem=andares_garagem,
                           proprietario=proprietario,
                           categoria_animal=categoria_animal,
                           proprietarios=proprietarios,
                           mapeamento_breadcrumbs=mapeamento_breadcrumbs)


@app.route('/imoveis/excluir/imovel/<int:id>', methods=['GET', 'POST'])
def excluirImovel(id):
    imovel = Imovel.query.get(id)

    if request.method == 'POST':
        if imovel:
            imovel.ativo = False
            db.session.commit()
            flash('Imóvel removido com sucesso!', 'success')
            return redirect(url_for('imoveis'))


"""

CRUD categoria_imovel

"""


@app.route('/imoveis/criar_imovel_categoria', methods=['GET', 'POST'])
def criarCategoriaImovel():
    return render_template('pages-imoveis/cadastrar_imovel.html')


@app.route('/imoveis/editar/imovel/categoria/id', methods=['GET', 'POST'])
def editarCategoriaImovel():
    return render_template('pages-imoveis/editar_imovel.html')


@app.route('/imoveis/excluir/imovel/categoria/id', methods=['GET', 'POST'])
def excluirCategoriaImovel():
    return redirect('imoveis')
