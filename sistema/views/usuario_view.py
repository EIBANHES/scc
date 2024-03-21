from sistema import app, db, flash, redirect, url_for, render_template, request, mapeamento_breadcrumbs, get_page_args, Pagination, current_user
from sistema.models.usuario_model import Usuario
from sistema.models.tipo_administrador import TipoAdministrador
from sistema import or_, desc
# Configurações


@app.route('/configuracoes/meu-perfil', methods=['GET', 'POST'])
def configMeuPerfil():
    tipo_adm = TipoAdministrador.query.all()
    if request.method == 'POST':
        current_user.nome = request.form['nome']
        current_user.email = request.form['email']
        current_user.cpf = request.form['cpf']
        current_user.cnpj = request.form['cnpj']
        current_user.razao_social = request.form['razao_social']
        current_user.numero_contato = request.form['celular-principal']
        current_user.tipo_administrador_id = request.form['tipo-adm']
        db.session.commit()
        flash('Usuário editado com sucesso', 'success')
        return redirect(url_for('configUsuarios'))
    return render_template('page-config/meu-perfil.html', mapeamento_breadcrumbs=mapeamento_breadcrumbs, tipo_adm=tipo_adm)


@app.route('/configuracoes/usuario', methods=['GET', 'POST'])
def configUsuarios():
    search_query = request.args.get('search')
    usuarios_query = Usuario.query.join(Usuario.tipo_administrador)
    ativo_filter = request.args.get('ativo-usuario')
    total = usuarios_query.count()
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')

    if search_query:
        usuarios_query = usuarios_query.filter(or_(
            Usuario.nome.ilike(f'%{search_query}%'),
            Usuario.email.ilike(f'%{search_query}%'),
            Usuario.numero_contato.ilike(f'%{search_query}%'),
            TipoAdministrador.tipo.ilike(f'%{search_query}%'),
        ))
    if ativo_filter:
        usuarios_query = usuarios_query.filter(
            Usuario.ativo == ativo_filter)

    # Ordenação baseada nos parâmetros recebidos
    order_by = request.args.get('order_by')
    order_direction = request.args.get('order_direction', 'asc')

    if order_by:
        if order_direction == 'asc':
            # Caso a ordenação seja por ordem crescente:
            if order_by == 'nome':
                usuarios_query = usuarios_query.order_by(Usuario.nome.asc())
            elif order_by == 'email':
                usuarios_query = usuarios_query.order_by(Usuario.email.asc())

        elif order_direction == 'desc':
            # Caso a ordenação seja por ordem decrescente:
            if order_by == 'nome':
                usuarios_query = usuarios_query.order_by(Usuario.nome.desc())
            elif order_by == 'email':
                usuarios_query = usuarios_query.order_by(Usuario.email.desc())

    # Tratamento para mudança de direção de ordenação ao usuário clicar novamente na tag (caso for 'desc', virará 'asc' e vice-versa)
    next_order_direction = 'asc' if order_direction == 'desc' else 'desc'

    # Setando novamente a ordenação pela data_criacao
    usuarios_query = usuarios_query.order_by(desc(Usuario.data_criacao))
    
    usuarios = usuarios_query.offset(offset).limit(per_page).all()

    pagination = Pagination(page=page, per_page=per_page,
                            offset=offset, total=total, css_framework='bootstrap')
    # Incrementando as páginas para ir para a próxima página
    next_page = pagination.page + 1
    # Decrementando as páginas para voltar uma página
    prev_page = pagination.page - 1

    return render_template('page-config/listagem-usuarios.html', mapeamento_breadcrumbs=mapeamento_breadcrumbs,
                           ativo_filter=ativo_filter,
                           pagination=pagination,
                           next_page=next_page,
                           prev_page=prev_page,
                           order_by=order_by,
                           order_direction=order_direction,
                           next_order_direction=next_order_direction,
                           usuarios=usuarios)


@app.route('/configuracoes/usuario/<int:id>/editar-usuario', methods=['GET', 'POST'])
def configEditarUsuario(id):
    usuario = Usuario.query.get(id)
    tipo_administrador = TipoAdministrador.query.all()
    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        usuario.cpf = request.form['cpf']
        usuario.cnpj = request.form['cnpj']
        usuario.razao_social = request.form['razao_social']
        usuario.numero_contato = request.form['numero-contato']
        usuario.tipo_administrador_id = request.form['tipo-administrador']

        if usuario.nome and usuario.email and usuario.cpf and usuario.numero_contato:
            db.session.commit()
            flash('Usuário editado com sucesso', 'success')
            return redirect(url_for('configUsuarios'))
        flash('Preencha todos os campos obrigatórios', 'danger')

    return render_template('page-config/editar-usuario.html', mapeamento_breadcrumbs=mapeamento_breadcrumbs, usuario=usuario, tipo_administrador=tipo_administrador)


@app.route('/configuracoes/usuario/<int:id>/excluir-usuario', methods=['GET', 'POST'])
def configExcluirUsuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.ativo = False
        db.session.commit()
        flash(f'Usuário {usuario.nome} excluido com sucesso', 'success')
        return redirect(url_for('configUsuarios'))
    return render_template('page-config/listagem-usuarios.html', mapeamento_breadcrumbs=mapeamento_breadcrumbs, usuario=usuario)


@app.route('/configuracoes/usuario/<int:id>/visualizar-usuario', methods=['GET', 'POST'])
def configVisualizarUsuario(id):
    usuario = Usuario.query.get(id)
    return render_template('page-config/visualizar-usuario.html', mapeamento_breadcrumbs=mapeamento_breadcrumbs, usuario=usuario)

# Fim Configurações
