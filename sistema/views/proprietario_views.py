from sistema import app, db, flash, redirect, url_for, render_template, request, mapeamento_breadcrumbs, get_page_args, Pagination
from sistema.models.pessoa_model import Pessoa
from sistema.models.morador_model import Morador
from sistema.models.imovel_model import Imovel
from sistema.models.andar_model import Andar
from sistema.utils.formata_data import validar_data_aniversario, formatar_data_brasil
from sistema import or_, asc, desc

# Proprietarios


@app.route('/proprietarios', methods=['GET', 'POST'])
def listaProprietarios():
    query_pesquisa = request.args.get('search')
    andar_filter = request.args.get('andar')
    apartamento_filter = request.args.get('apartamento')
    email_filter = request.args.get('email')

    entity_name = "proprietarios"

    proprietarios_query = Pessoa.query.filter(
        Pessoa.tipo_morador_id.is_(None),
        Pessoa.ativo.is_(True)
    ).join(Pessoa.imoveis).group_by(Pessoa.nome)

    if query_pesquisa:
        proprietarios_query = proprietarios_query.filter(or_(
            Pessoa.nome.ilike(f'%{query_pesquisa}%'),
            Pessoa.cpf.ilike(f'%{query_pesquisa}%'),
            Pessoa.rg.ilike(f'%{query_pesquisa}%')
        ))

    if andar_filter:
        proprietarios_query = proprietarios_query.filter(
            Imovel.andar_id == andar_filter
        )

    if apartamento_filter:
        proprietarios_query = proprietarios_query.filter(
            Imovel.apartamento.ilike(f'%{apartamento_filter}%')
        )

    if email_filter:
        proprietarios_query = proprietarios_query.filter(
            Pessoa.email.ilike(f'%{email_filter}%')
        )

    total = proprietarios_query.count()

    page, per_page, _ = get_page_args(
        page_parameter='page', per_page_parameter='per_page'
    )

    pagination = Pagination(
        page=page, per_page=per_page, total=total, css_framework='bootstrap'
    )

    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction', 'asc')

    if order_by:
        if order_direction == 'asc':
            if order_by == 'nome':
                proprietarios_query = proprietarios_query.order_by(
                    Pessoa.nome.asc()
                )
        elif order_direction == 'desc':
            if order_by == 'nome':
                proprietarios_query = proprietarios_query.order_by(
                    Pessoa.nome.desc()
                )

    next_order_direction = 'asc' if order_direction == 'desc' else 'desc'

    next_page = pagination.page + 1
    prev_page = pagination.page - 1

    proprietarios = proprietarios_query.order_by(
        desc(Pessoa.data_criacao)).offset(
        (page - 1) * per_page).limit(per_page).all()

    return render_template(
        'pages-proprietario/listagem-proprietarios.html',
        mapeamento_breadcrumbs=mapeamento_breadcrumbs,
        proprietarios=proprietarios,
        andar_query=Andar.query.all(),
        pagination=pagination,
        next_page=next_page,
        prev_page=prev_page,
        order_by=order_by,
        order_direction=order_direction,
        next_order_direction=next_order_direction,
        entity_name=entity_name,
        formatar_data_brasil=formatar_data_brasil
    )


@app.route('/gestao-moradores/proprietarios/cadastrar-proprietario', methods=['GET', 'POST'])
def criarProprietario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        rg = request.form['rg']
        data_nascimento = request.form['data-nascimento']
        profissao = request.form['profissao']
        numero_principal = request.form['celular-principal']
        numero_secundario = request.form['celular-secundario']
        tipo_morador_id = None

        # Verificação para ver se o CPF, RG e e-mail já estão cadastrados no banco
        cpf_existe = Pessoa.query.filter_by(cpf=cpf).first()
        rg_existe = Pessoa.query.filter_by(rg=rg).first()
        email_existe = Pessoa.query.filter_by(email=email).first()

        if cpf_existe or rg_existe or email_existe:
            flash(
                'O proprietário que você está tentando cadastrar já existe. Tente novamente.', 'danger')
            return redirect(url_for('criarProprietario'))

        if nome and cpf and rg and data_nascimento and profissao and numero_principal:
            # Condição para caso o usuário digite um nome em minúsculo
            if nome.islower():
                # Transformando a primeira letra com CAPS LOCK
                nome = nome.capitalize()

            # Condição para caso o usuário digite um nome em letra maiúscula
            elif nome.isupper():
                nome = nome.capitalize()

            # Condição para caso o usuário digite a profissão em minúsculo
            if profissao.islower():
                # Transformando a primeira letra com CAPS LOCK
                profissao = profissao.capitalize()

            # Condição para caso o usuário digite a profissão em letra maiúscula
            elif profissao.isupper():
                profissao = profissao.capitalize()

            proprietario = Pessoa(nome, email, cpf, rg, data_nascimento, profissao,
                                  numero_principal, numero_secundario, tipo_morador_id)

            try:
                db.session.add(proprietario)
                db.session.commit()
                flash('Proprietário cadastrado com sucesso', 'success')
                return redirect(url_for('imoveis'))
            except:
                flash('Erro ao cadastrar proprietario', 'warning')
        else:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return redirect(url_for('criarProprietario'))

    return render_template('pages-proprietario/criar-proprietario.html', mapeamento_breadcrumbs=mapeamento_breadcrumbs)


@app.route('/gestao-moradores/proprietarios/<int:id>/editar-proprietario', methods=['GET', 'POST'])
def editarProprietario(id):
    pessoa = Pessoa.query.get(id)
    imovel = Imovel.query.filter_by(pessoa_id=pessoa.id).first()
    lista_imovel = Imovel.query.all()
    if request.method == 'POST':
        pessoa.nome = request.form['nome']
        pessoa.email = request.form['email']
        pessoa.cpf = request.form['cpf']
        pessoa.rg = request.form['rg']
        pessoa.data_nascimento = request.form['data-nascimento']
        pessoa.profissao = request.form['profissao']
        pessoa.numero_principal = request.form['celular-principal']
        pessoa.numero_secundario = request.form['celular-secundario']

        db.session.commit()
        # flash('Proprietário editado com sucesso', 'success')
        return redirect(url_for('listaProprietarios'))
    return render_template('pages-proprietario/editar-proprietario.html', mapeamento_breadcrumbs=mapeamento_breadcrumbs, pessoa=pessoa, imovel=imovel, lista_imovel=lista_imovel)


@app.route('/gestao-moradores/proprietarios/<int:id>/excluir-proprietario', methods=['GET', 'POST'])
def excluirProprietario(id):
    proprietario = Pessoa.query.get(id)
    imoveis = Imovel.query.filter_by(pessoa_id=proprietario.id).all()

    if request.method == 'POST':
        proprietario.ativo = False
        for imovel in imoveis:
            imovel.ativo = False
        db.session.commit()
        flash(
            f'O(a) proprietario(a) {proprietario.nome} foi excluido(a) com sucesso', 'success')
        return redirect(url_for('listaProprietarios'))

    return render_template('pages-proprietario/listagem-proprietarios.html', mapeamento_breadcrumbs=mapeamento_breadcrumbs, proprietarios=proprietario)

@app.route('/gestao-moradores/proprietarios/<int:id>/visualizar-proprietario', methods=['GET', 'POST'])
def visualizarProprietario(id):
    proprietario = Pessoa.query.get(id)
    imovel = proprietario.imoveis
    return render_template('pages-proprietario/visualizar-proprietario.html', mapeamento_breadcrumbs=mapeamento_breadcrumbs, proprietario=proprietario, imovel=imovel)
