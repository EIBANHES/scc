from flask import Flask, render_template, request, redirect, flash, url_for, make_response, jsonify, send_file, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_paginate import Pagination, get_page_args
from flask_login import LoginManager, login_user, logout_user, current_user
from sqlalchemy import or_, asc, desc
import requests
from config import caminho_wkhtmltopdf
import pdfkit
from config import caminho_wkhtmltopdf
from gerencianet import Gerencianet

# Credenciais de hml
# CREDENTIALS = {
#     'client_id': 'Client_Id_419ec832ecfa276c7225544b53581e1942c79739',
#     'client_secret': 'Client_Secret_1ad5c1c7bb49fb446cfe00f05f1d4a25a5518795',
#     'sandbox': True,
#     'certificate': 'sistema/static/certificado-homologacao.pem'
# }

# Credenciais de Prod
CREDENTIALS = {
    'client_id': 'Client_Id_800df4436357faa453b8e1fa35b97dfbb4dda251',
    'client_secret': 'Client_Secret_5fb7b5671429b1c251f046ae5167c090502ff4f0',
    'sandbox': False,
    'certificate': 'sistema/static/certificado-producao.pem'
}

# Instancia gn
gn = Gerencianet(CREDENTIALS)

app = Flask(__name__)
app.secret_key = "eu como o cu do rodrigo até ele pedir leitinho na bokinha"
app.config.from_object('config')

# Instancia SQLAlchemy
db = SQLAlchemy(app)

# Instancia Migrate
migrate = Migrate(app, db)

# Login
login_manager = LoginManager(app)

# Configurando o 'pdfkit' com o caminho do 'wkhtmltopdf'
pdfkit_config = pdfkit.configuration(wkhtmltopdf=caminho_wkhtmltopdf)

# Dicionário de mapeamento das breadcrumbs:
mapeamento_breadcrumbs = {
    # Moradores
    'Home': {
        'func': 'listaProprietarios',
        'icon': 'fa-sharp fa-light fa-house'
    },
    'Condominios': {
        'func': 'condominios',
        'icon': 'fa-regular fa-building'
    },
    'Criar condomínio': {
        'func': 'cadastrarCondominio',
        'icon': 'fa-regular fa-building'
    },
    'Moradores': {
        'func': 'listaMorador',
        'icon': 'fa-sharp fa-light fa-users'
    },
    'Cadastro de moradores': {
        'func': 'criarMorador',
        'icon': 'fa-sharp fa-light fa-users'
    },
    'Editar morador': {
        'func': 'editarMorador',
        'icon': 'fa-sharp fa-light fa-users'
    },

    'Visualizar morador': {
        'func': 'visualizarMorador',
        'icon': 'fa-sharp fa-light fa-users'
    },
    # Proprietários
    'Proprietários': {
        'func': 'listaProprietarios',
        'icon': 'fa-sharp fa-light fa-users'
    },
    'Cadastro de proprietário': {
        'func': 'criarProprietario',
        'icon': 'fa-sharp fa-light fa-users'
    },
    'Editar proprietário': {
        'func': 'editarProprietario',
        'icon': 'fa-sharp fa-light fa-users'
    },
    'Visualizar proprietário': {
        'func': 'visualizarProprietario',
        'icon': 'fa-sharp fa-light fa-users'
    },
    # Configurações
    'Configurações': {
        'func': 'configUsuarios',
        'icon': 'fa-sharp fa-light fa-gear'
    },
    'Meu perfil': {
        'func': 'configPerfil',
        'icon': 'fa-sharp fa-light fa-user'
    },
    'Usuários': {
        'func': 'configUsuarios',
        'icon': 'fa-sharp fa-light fa-users'
    },
    'Cadastro de Usuários': {
        'func': 'cadastro',
        'icon': 'fa-sharp fa-light fa-users'
    },
    # Imóveis
    'Imóveis': {
        'func': 'imoveis',
        'icon': 'fa-sharp fa-light fa-building'
    },
    'Cadastrar imóvel': {
        'func': 'cadastrarImovel',
        'icon': 'fa-sharp fa-light fa-building'
    },
    'Editar imóvel': {
        'func': 'editarImovel',
        'icon': 'fa-sharp fa-light fa-building'
    },
    'Visualizar imóvel': {
        'func': 'visualizarImovel',
        'icon': 'fa-sharp fa-light fa-building'
    },
    # Almoxarifado
    'Almoxarifado': {
        'func': 'almoxarifado',
        'icon': 'fa-sharp fa-light fa-warehouse'
    },
    'Produtos': {
        'func': 'almoxarifado',
        'icon': 'fa-sharp fa-light fa-box'
    },
    'Cadastrar produto': {
        'func': 'criarProduto',
        'icon': 'fa-sharp fa-light fa-box'
    },
    'Editar produto': {
        'func': 'editarProduto',
        'icon': 'fa-sharp fa-light fa-box'
    },
    'Visualizar produto': {
        'func': 'visualizarProduto',
        'icon': 'fa-sharp fa-light fa-box'
    },
    #Movimentações Almoxarifado
    'Movimentações': {
        'func': 'listagemMovimentacoes',
        'icon': 'fa-sharp fa-light fa-exchange'
    },
    #Observações
    'Observações': {
        'func': 'observacoes',
        'icon': 'fa-sharp fa-light fa-memo'
    },
    'Criar observação': {
        'func': 'criarObservacao',
        'icon': 'fa-sharp fa-light fa-memo'
    },
    'Editar observação': {
        'func': 'editarObservacao',
        'icon': 'fa-sharp fa-light fa-memo'
    } ,
    #Pagamentos
    'Meus Pagamentos': {
        'func': 'meusPagamentos',
        'icon': 'fa-sharp fa-light fa-sack-dollar'
    },
    #Gerencianet
    'Formas de Pagamento': {
        'func': 'formasPagamento',
        'icon': 'fa-sharp fa-light fa-money-bill'
    },
    'Pix': {
        'func': 'formasPagamento',
        'icon': 'fa-sharp fa-light fa-money-bill'
    },
    'Pagar por pix': {
        'func': 'pagamentoPix',
        'icon': 'fa-sharp fa-light fa-money-bill'
    }
}

from sistema.views import (
    gerencianet_views,
    imoveis_views,
    almoxarifado_views,
    cadastro_condominio,
    proprietario_views,
    morador_views,
    usuario_view,
    index,
    observacao_views,
    pagamentos_views
)

from sistema.models import (
    pessoa_model,
    tipo_administrador,
    tipo_morador_model,
    tipo_animal_model,
    morador_model,
    almoxarifado_model,
    categoria_produto_model,
    imovel_model,
    usuario_model,
    andar_model,
    tipo_garagem_model,
    observacao_model,
    produto_movimentacoes_model,
)
