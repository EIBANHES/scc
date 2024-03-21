from sistema import app, db, render_template, mapeamento_breadcrumbs, Pagination, session
from ..views.gerencianet_views import detalharListaCobrancaPix

@app.route('/meus-pagamentos', methods=['GET', 'POST'])
def meusPagamentos():
    
    detalhar_response = detalharListaCobrancaPix()
    lista_pix_dados = detalhar_response['data'] 

    return render_template('pages-pagamentos/meus-pagamentos.html', data=lista_pix_dados, 
                           mapeamento_breadcrumbs=mapeamento_breadcrumbs)