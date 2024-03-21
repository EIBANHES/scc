from sistema import app, db, render_template, redirect, url_for, flash, request, mapeamento_breadcrumbs, get_page_args, Pagination

@app.route('/index', methods=['GET', 'POST'])
def condominios():
    return render_template('pages-condominio/listagem-condominio.html');

@app.route('/cadastrar-condominio', methods=['GET', 'POST'])
def cadastrarCondominio():
    return render_template('pages-condominio/cadastrar-condominio.html', mapeamento_breadcrumbs=mapeamento_breadcrumbs);