from sistema import app, db, render_template, redirect, url_for, flash, request, mapeamento_breadcrumbs, get_page_args, Pagination
from sistema.models.pessoa_model import Pessoa
from sistema.models.morador_model import Morador
from sistema.models.imovel_model import Imovel
from sistema.models.tipo_morador_model import TipoMorador
from sistema.models.andar_model import Andar
from sistema.utils.formata_data import validar_data_aniversario
from sistema import or_, desc


@app.route('/gestao-moradores/listar-moradores', methods=['GET', 'POST'])
def listaMorador():
    search_query = request.args.get('search')
    email_filter = request.args.get('email')
    tipo_morador = TipoMorador.query.all()
    morador_query = Morador.query.filter_by(ativo=True).join(
        Morador.pessoa).join(Morador.tipo_morador)
    total = morador_query.count()

    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')

    if search_query:
        morador_query = morador_query.filter(or_(
            Pessoa.nome.ilike(f'%{search_query}%'),
            Pessoa.cpf.ilike(f'%{search_query}%'),
            Pessoa.rg.ilike(f'%{search_query}%'),
            TipoMorador.tipo.ilike(f'%{search_query}%')
        ))

    if email_filter:
        morador_query = morador_query.filter(
            Pessoa.email.ilike(f'%{email_filter}%'))
        
    # Ordenação baseada nos parâmetros recebidos
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction', 'asc')
    
    if order_by:
        if order_direction == 'asc':
            # Caso a ordenação seja por ordem crescente:
            if order_by == 'nome':
                morador_query = morador_query.order_by(Pessoa.nome.asc())

        elif order_direction == 'desc':
            # Caso a ordenação seja por ordem decrescente:
            if order_by == 'nome':
                morador_query = morador_query.order_by(Pessoa.nome.desc())

    # Tratamento para mudança de direção de ordenação ao usuário clicar novamente na tag (caso for 'desc', virará 'asc' e vice-versa)
    next_order_direction = 'asc' if order_direction == 'desc' else 'desc'

    #Atualizando a totalidade de moradores (contador) 
    total = morador_query.count()
    # Setando novamente a ordenação pela data_criacao
    morador_query = morador_query.order_by(desc(Morador.data_criacao))
    moradores = morador_query.limit(per_page).all()

    pagination = Pagination(page=page, offset=offset,
                            per_page=per_page, total=total, css_framework='bootstrap')
    #Incrementando as páginas para ir para a próxima página
    next_page = pagination.page + 1 
    #Decrementando as páginas para voltar uma página
    prev_page = pagination.page - 1

    return render_template('pages-morador/listagem-morador.html', mapeamento_breadcrumbs=mapeamento_breadcrumbs,
                           tipo_morador=tipo_morador,
                           pagination=pagination,
                           next_page=next_page,
                           prev_page=prev_page,
                           order_by=order_by,
                           order_direction=order_direction,
                           next_order_direction=next_order_direction,
                           moradores=moradores)


@app.route('/gestao-moradores/criar-morador', methods=['GET', 'POST'])
def criarMorador():
    tipoMorador = TipoMorador.query.all()

    imoveis = Imovel.query.all()
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        rg = request.form['rg']
        data_nascimento = request.form['data-nascimento']
        profissao = request.form['profissao']
        numero_principal = request.form['celular-principal']
        numero_secundario = request.form['celular-secundario']
        tipo_morador_id = request.form['tipo-morador']
        imovel_id = request.form.get('residencia')


        # Verificação para ver se o CPF, RG e e-mail já estão cadastrados no banco
        cpf_existe = db.session.query(Morador).join(Morador.pessoa).filter(Pessoa.cpf == cpf).first()
        rg_existe = db.session.query(Morador).join(Morador.pessoa).filter(Pessoa.rg == rg).first()
        email_existe = db.session.query(Morador).join(Morador.pessoa).filter(Pessoa.email == email).first()

        if cpf_existe or rg_existe or email_existe:
            flash('O morador que você está tentando cadastrar já existe. Tente novamente.', 'danger')
            return redirect(url_for('criarMorador'))
        
        if nome and email and cpf and rg and data_nascimento and profissao and numero_principal and tipo_morador_id != '0' and imovel_id != '0':
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

            pessoa_info = Pessoa(nome, email, cpf, rg, data_nascimento, profissao, numero_principal, numero_secundario,
                                 tipo_morador_id)
            try:
                db.session.add(pessoa_info)
                db.session.commit()
                morador_info = Morador(
                    pessoa_info.id, tipo_morador_id, imovel_id)
                db.session.add(morador_info)
                db.session.commit()
                flash('Morador cadastrado com sucesso', 'success')
                return redirect(url_for('listaMorador'))
            except:
                flash('Erro ao cadastrar morador', 'danger')
        else:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return redirect(url_for('criarMorador'))
    return render_template('pages-morador/criar-morador.html', mapeamento_breadcrumbs=mapeamento_breadcrumbs, tipoMorador=tipoMorador, imoveis=imoveis)


@app.route('/gestao-moradores/morador/<int:id>/editar-morador', methods=['GET', 'POST'])
def editarMorador(id):
    morador = Morador.query.get(id)
    tipo_morador = TipoMorador.query.all()
    imoveis = Imovel.query.all()

    if request.method == 'POST':
        morador.pessoa.nome = request.form['nome']
        morador.pessoa.email = request.form['email']
        morador.pessoa.cpf = request.form['cpf']
        morador.pessoa.rg = request.form['rg']
        morador.pessoa.data_nascimento = request.form['data-nascimento']
        morador.pessoa.profissao = request.form['profissao']
        morador.pessoa.numero_principal = request.form['celular-principal']
        morador.pessoa.numero_secundario = request.form['celular-secundario']
        morador.imovel_id = request.form['residencia']
        morador.tipo_morador_id = request.form.get('tipo-morador')

        db.session.commit()
        flash('Morador editado com sucesso', 'success')
        return redirect(url_for('listaMorador'))
    return render_template('pages-morador/editar-morador.html', mapeamento_breadcrumbs=mapeamento_breadcrumbs, morador=morador, tipo_morador=tipo_morador, imoveis=imoveis)


@app.route('/gestao-moradores/morador/<int:id>/excluir-morador', methods=['GET', 'POST'])
def excluirMorador(id):
    morador = Morador.query.get(id)

    if request.method == 'POST':
        morador.ativo = False
        morador.pessoa.ativo = False
        db.session.commit()
        flash(
            f'O(a) morador(a) { morador.pessoa.nome } foi excluido(a) com sucesso', 'success')
        return redirect(url_for('listaMorador'))
    return render_template('pages-morador/listagem-morador.html', mapeamento_breadcrumbs=mapeamento_breadcrumbs, morador=morador)


@app.route('/gestao-moradores/morador/<int:id>/visualizar-morador', methods=['GET', 'POST'])
def visualizarMorador(id):
    morador = Morador.query.get(id)
    proprietario = morador.imovel.pessoa_imovel
    return render_template('pages-morador/visualizar-morador.html', mapeamento_breadcrumbs=mapeamento_breadcrumbs, morador=morador, proprietario=proprietario)
