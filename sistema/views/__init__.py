from sistema import app, db, redirect, render_template, url_for, flash, make_response, pdfkit, request, mapeamento_breadcrumbs, get_page_args, Pagination, jsonify
from sistema import login_user, logout_user
from sistema.models.tipo_administrador import TipoAdministrador
from sistema.models.usuario_model import Usuario
from sistema.models.morador_model import Morador
from sistema.models.pessoa_model import Pessoa
from sistema.models.imovel_model import Imovel
from sistema.models.andar_model import Andar
from sistema.models.observacao_model import Observacao
from sistema.models.almoxarifado_model import Almoxarifado
from sistema import pdfkit_config
from sistema.utils.formata_data import validar_data_aniversario, formatar_data_brasil
from sistema.utils.formata_valor import formatacao_valor_numerico
from sistema import or_, desc
from flask import abort
from sistema import gn


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cpf_cnpj = request.form['cpf_cnpj']
        senha = request.form['senha']

        if len(cpf_cnpj) == 14:
            cpf = cpf_cnpj
            # Verificação para ver se o CPF/CNPJ já estão cadastrados no banco
            usuario = Usuario.query.filter_by(cpf=cpf).first()
        elif len(cpf_cnpj) == 18:
            cnpj = cpf_cnpj
            # Verificação para ver se o CPF/CNPJ já estão cadastrados no banco
            usuario = Usuario.query.filter_by(cnpj=cnpj).first()
        else:
            flash('CPF/CNPJ inválido.', 'danger')
            return redirect(url_for('index'))
        

        if not usuario or not usuario.verificaSenha(senha):
            flash('Usuário ou senha incorretos.', 'danger')
            return redirect(url_for('index'))
        else:
            try:
                if not usuario.ativo:
                    flash('Usuário sem permissão de acesso.', 'danger')
                else:
                    login_user(usuario)
                    return redirect(url_for('listaProprietarios'))
            except:
                flash('Erro ao realizar login.', 'danger')
                return redirect(url_for('index'))

    return render_template("login/login.html")

@app.route('/cadastrar-usuario', methods=['GET', 'POST'])
def cadastrarUsuario():
    tipo_administrador = TipoAdministrador.query.all()
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        cnpj = request.form['cnpj']
        razao_social = request.form['razao_social']
        numero_contato = request.form['celular-principal']
        tipo_administrador_id = request.form['tipo-administrador']
        senha = request.form['senha']
        
        # Verificação para ver se o CPF e E-mail já estão cadastrados no banco
        usuario_existente = Usuario.query.filter_by(email=email).first()

        # Caso o usuário não informe o CNPJ ou razão social, o valor setado será nulo
        if not cnpj or not razao_social:
            cnpj = None
            razao_social = ""

        # Verificação para ver se o CPF/CNPJ já estão cadastrados no banco
        cpf_cnpj_existe = Usuario.query.filter_by(cpf=cpf, cnpj=cnpj).first()

        if nome and cpf and numero_contato and tipo_administrador_id != '0' and senha:
            if usuario_existente:
                if usuario_existente.ativo:
                    flash('Este e-mail já está sendo utilizado.', 'danger')
                else:
                    flash('Este e-mail pertence a um usuário excluído.', 'danger')

            elif cpf_cnpj_existe:
                    flash('O CPF/CNPJ informado já tem um cadastro ativo no sistema. Tente novamente.', 'danger')

            else:
                try:
                    # Condição para caso o usuário digite um nome em minúsculo
                    if nome.islower():
                        nome = nome.capitalize()  # Transformando a primeira letra com CAPS LOCK

                    # Condição para caso o usuário digite um nome em letra maiúscula
                    elif nome.isupper():
                        nome = nome.capitalize()  # Transformando a primeira letra com CAPS LOCK

                    usuario = Usuario(
                        nome, razao_social, email, cpf, cnpj, numero_contato, tipo_administrador_id, senha)
                    db.session.add(usuario)
                    db.session.commit()
                    flash('Usuário cadastrado com sucesso.', 'success')
                    return redirect(url_for('configUsuarios'))
                except:
                    flash('Ocorreu um erro ao cadastrar o usuário.', 'danger')
        else:
            flash('Preencha todos os campos obrigatórios.', 'danger')

    return render_template("login/cadastrar-se.html", tipo_administrador=tipo_administrador, mapeamento_breadcrumbs=mapeamento_breadcrumbs)


@app.route('/cadastrar-se', methods=['GET', 'POST'])
def cadastrarSe():
    tipo_administrador = TipoAdministrador.query.all()
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        cnpj = request.form['cnpj']
        razao_social = request.form['razao_social']
        numero_contato = request.form['celular-principal']
        tipo_administrador_id = request.form['tipo-administrador']
        senha = request.form['senha']
        # Verificação para ver se o e-mail já está cadastrado no banco
        usuario_existente = Usuario.query.filter_by(email=email).first()

        # Caso o usuário não informe o CNPJ ou razão social, o valor setado será nulo
        if not cnpj or not razao_social:
            cnpj = None
            razao_social = ""
        
        # Verificação para ver se o CPF/CNPJ já estão cadastrados no banco
        cpf_cnpj_existe = Usuario.query.filter_by(cpf=cpf, cnpj=cnpj).first()

        if nome and cpf and numero_contato and tipo_administrador_id != '0' and senha:
            if usuario_existente:
                if usuario_existente.ativo:
                    flash('Este e-mail já está sendo utilizado.', 'danger')
                else:
                    flash('Este e-mail pertence a um usuário excluído.', 'danger')

            elif cpf_cnpj_existe:
                    flash('O CPF/CNPJ informado já tem um cadastro ativo no sistema. Tente novamente.', 'danger')

            else:
                try:
                    # Condição para caso o usuário digite um nome em minúsculo
                    if nome.islower():
                        nome = nome.capitalize()  # Transformando a primeira letra com CAPS LOCK

                    # Condição para caso o usuário digite um nome em letra maiúscula
                    elif nome.isupper():
                        nome = nome.capitalize()  # Transformando a primeira letra com CAPS LOCK

                    usuario = Usuario(
                        nome, razao_social, email, cpf, cnpj, numero_contato, tipo_administrador_id, senha)
                    db.session.add(usuario)
                    db.session.commit()
                    flash('Usuário cadastrado com sucesso.', 'success')
                    return redirect(url_for('index'))
                except:
                    flash('Ocorreu um erro ao cadastrar o usuário.', 'danger')
        else:
            flash('Preencha todos os campos obrigatórios.', 'danger')

    return render_template("login/cadastro-login.html", tipo_administrador=tipo_administrador, mapeamento_breadcrumbs=mapeamento_breadcrumbs)


@app.route('/sair')
def logout():
    logout_user()
    flash('Usuário deslogado com sucesso', 'success')
    return redirect(url_for('index'))


@app.route('/404')
def notFound():
    return render_template('error_404.html')


@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('notFound'))

# Função para manipular e receber os parâmetros, gerando o body HTML e depois rendenizando/criando o PDF
def exportar_pdf(entity_name, query, template_name, proprietarios):
    html = render_template(
        template_name,
        items=query.all(),
        entity_name=entity_name,
        formatar_data_brasil=formatar_data_brasil,
        formatacao_valor_numerico=formatacao_valor_numerico,
        proprietarios=proprietarios
    )

    pdf = pdfkit.from_string(html, False, configuration=pdfkit_config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=listagem_{entity_name}.pdf'

    return response

# Mapeando no dicionário os nomes das entidades (CRUDS) para serem exportadas
query_builders = {
    'imoveis': lambda query_pesquisa, andar_filter, apartamento_filter, order_by, order_direction: Imovel.query.filter_by(ativo=True).join(Pessoa.imoveis).join(Andar).order_by(desc(Imovel.data_criacao)),
    'proprietarios': lambda query_pesquisa, andar_filter, apartamento_filter, email_filter, order_by, order_direction: Pessoa.query.filter(Pessoa.tipo_morador_id.is_(None), Pessoa.ativo.is_(True)).join(Pessoa.imoveis).order_by(desc(Pessoa.data_criacao)),
    'moradores': lambda query_pesquisa, email_filter, order_by, order_direction: Morador.query.filter_by(ativo=True).join(Morador.pessoa).join(Morador.tipo_morador).order_by(desc(Morador.data_criacao)), 
    'produtos': lambda query_pesquisa, categoria_filter, order_by, order_direction: Almoxarifado.query.filter_by(ativo=True).order_by(desc(Almoxarifado.data_criacao)),
    'usuarios': lambda query_pesquisa, ativo_filter, order_by, order_direction: Usuario.query.join(Usuario.tipo_administrador).order_by(desc(Usuario.data_criacao)),
    'observacoes': lambda query_pesquisa: Observacao.query.filter_by(ativo=True).order_by(desc(Observacao.data_criacao)), 
}


@app.route('/exportar/<string:entity_name>/pdf', methods=['GET'])
def exportar_pdf_rota(entity_name):
    query_pesquisa = request.args.get('search')
    andar_filter = request.args.get('andar')
    apartamento_filter = request.args.get('apartamento')
    email_filter = request.args.get('email')
    categoria_filter = request.args.get('categoria-produto')
    ativo_filter = request.args.get('ativo-usuario')
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction', 'asc')

    # Condição 404 para caso a entidade não esteja mapeada no dicionário
    if entity_name not in query_builders:
        abort(404)

    # Pegando UMA ÚNICA query_builder com base no nome da entidade mapeada fornecida pelo usuário
    query_builder = query_builders[entity_name]

    if entity_name == 'imoveis':
        query = query_builder(query_pesquisa, andar_filter, apartamento_filter, order_by, order_direction)
        
    elif entity_name == 'moradores':
        query = query_builder(query_pesquisa, email_filter, order_by, order_direction)

    elif entity_name == 'produtos':
        query = query_builder(query_pesquisa, categoria_filter, order_by, order_direction)
    
    elif entity_name == 'usuarios':
        query = query_builder(query_pesquisa, ativo_filter, order_by, order_direction)

    elif entity_name == 'observacoes':
        query = query_builder(query_pesquisa)

    #Proprietários
    else:
        query = query_builder(query_pesquisa, andar_filter, apartamento_filter, email_filter, order_by, order_direction)

    # Setando o nome do template com base no HTML
    template_name = f'template_pdf.html'

    # Pegando a listagem de proprietários para mostrar ele no HTML de template do PDF sem erros (necessário para listar corretamente)
    proprietarios = Pessoa.query.filter(Pessoa.tipo_morador_id.is_(None), Pessoa.ativo.is_(True)).join(Pessoa.imoveis).all()

    return exportar_pdf(entity_name, query, template_name, proprietarios)



