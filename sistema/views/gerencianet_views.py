from sistema import app, db, gn, render_template, request, mapeamento_breadcrumbs, jsonify, session
from sistema.utils.formata_data import formatar_data, formatar_apenas_data
from sistema.utils.formata_cnpj import formatar_cnpj
from sistema.utils.formata_cpf import formatar_cpf
from sistema.utils.gerencianet_api import criar_cobranca_pix
from sistema.utils.gerencianet_api import cria_qrcode_pix
from sistema.utils.formata_valor import formatacao_valor_numerico
from flask_login import current_user


@app.route('/forma-pagamento', methods=['GET', 'POST'])
def formasPagamento():
    boleto_dados = session.get('boleto_dados', {})

    return render_template('gerencianet/opcoes-pagamento.html', data=boleto_dados, 
                           formatar_apenas_data=formatar_apenas_data,
                           formatacao_valor_numerico=formatacao_valor_numerico,
                           mapeamento_breadcrumbs=mapeamento_breadcrumbs)


@app.route('/pix', methods=['GET', 'POST'])
def requestPix():
    nome = current_user.nome
    cpf = '083.975.211-35' # current_user.cpf Verificar se o CPF realmente existe, caso contrário, dará erro no ['loc']
    numero_contato = current_user.numero_contato
    cpf_numerico = ''.join(filter(str.isdigit, cpf))
    body = {
        'calendario': {
            'expiracao': 3600
        },
        'devedor': {
            'cpf': cpf_numerico,
            'nome': nome
        },
        'valor': {
            'original': '0.01'
        },
        'chave': '47728c1f-5e22-48d8-b328-bb391ba61c06',
        'solicitacaoPagador': 'Cobrança dos serviços prestados.'
    }

    response = criar_cobranca_pix()

    id_pix = response['loc']['id']
    valor_pix = response['valor']['original']
    data_criacao = response['calendario']['criacao']
    data_formatada = formatar_data(data_criacao)
    txid = response['txid']

    params = {'txid': txid}
    consulta = gn.pix_detail_charge(params=params)
    status_pagamento = consulta['status']

    copia_cola = cria_qrcode_pix(response, id_pix)

    return render_template('gerencianet/pix.html', mapeamento_breadcrumbs=mapeamento_breadcrumbs, txid=txid, qr_code_image="imagens/qrCodeImage.png", id_pix=id_pix, data_formatada=data_formatada, copia_cola=copia_cola, valor_pix=valor_pix, nome=current_user.nome, cpf=current_user.cpf, numero_contato=current_user.numero_contato, status_pagamento=status_pagamento)


@app.route('/detalhar_cobranca/pix/<string:tx_id>')
def detalharCobrancaPixPorId(tx_id):
    params = {
        'txid': tx_id
    }

    response =  gn.pix_detail_charge(params=params)
    print(response)

    return jsonify({"response" : response}) 

@app.route('/detalhar_lista_cobrancas/pix', methods=['GET'])
def detalharListaCobrancaPix():
    params = {
        "inicio": "2023-08-01T16:01:35Z",
        "fim": "2023-08-23T16:01:35Z"
    }

    response =  gn.pix_list_charges(params=params)
    #Criando dicionário responsável por reter todos dados da response
    data = {
        "status": response['cobs'][0]['status'],
        "data_criacao": response['cobs'][0]['calendario']['criacao'],
        "cliente_nome": response['cobs'][0]['devedor']['nome'],
        "cliente_cpf": response['cobs'][0]['devedor']['cpf'],
        "valor_total": response['cobs'][0]['valor']['original'],
        "tx_id": response['cobs'][0]['txid'],
    }
    
    
    # Armazenando os dados do dicionário em uma variável session (armazenar temporariamente, sem ter que criar outra rota)
    session['lista_pix_dados'] = data

    return {"response" : response, "data": data}


# @app.route('/detalhar_lista_cobrancas/pix/<string:inicio>/<string:fim>')
# def detalharListaCobrancaPix(inicio, fim):
#     params = { #Data em formato ISO-8601 (converter corretamente)
#         "inicio": inicio,
#         "fim": fim
#     }

#     response =  gn.pix_list_charges(params=params)
#     print(response)

#     return jsonify({"response" : response}) 

@app.route('/detalhar_lista_recebidos/pix')
def detalharListaPixRecebidos():
    params = { #Data em formato ISO-8601 (converter corretamente)
        "inicio": "2023-08-01T16:01:35Z",
        "fim": "2023-08-20T16:01:35Z"
    }

    response =  gn.pix_received_list(params=params)
    print(response)

    return jsonify({"response" : response}) 


@app.route('/pagamento-pix', methods=['GET', 'POST'])
def pagamentoPix():
    return render_template('gerencianet/pagamentopix.html', mapeamento_breadcrumbs=mapeamento_breadcrumbs)


@app.route('/pagamentos/gerar/boleto', methods=['POST'])
def gerarBoleto():
    data = request.json

    items = [
        {
            'name': 'Produto',
            'value': 100,  # Valor em centavos
            'amount': 1
        },
        {
            'name': 'Produto 2',
            'value': 100,  # Valor em centavos
            'amount': 2
        }
    ]

    shippings = [
        {
            'name': "Default Shipping Cost",
            'value': 100  # Valor em centavos
        }
    ]

    payment = {
        'payment': {
            'banking_billet': {
                'expire_at': '2023-08-30',
                'customer': {  # Dados do cliente
                    'name': "Gorbadoc Oldbuck",
                    'email': "gorb.oldbuck@gerencianet.com.br",
                    'cpf': "14014603059",
                    'birth': "1977-01-15",
                    'phone_number': "62986070247",
                }
            }
        }
    }

    #corporate_name = data.get('juridical_person', {}).get('corporate_name', '') # Pegar os dados de forma dinâmica 
    #cnpj = data.get('juridical_person', {}).get('cnpj', '')  # Pegar os dados de forma dinâmica

    corporate_name = 'Company'
    cnpj = '99794567000144'

    #Validando se os campos exxistem
    if corporate_name and cnpj:
        payment['payment']['banking_billet']['customer']['juridical_person'] = {
            'corporate_name': corporate_name,
            'cnpj': cnpj
        }

    body = {
        'items': items,
        'shippings': shippings
    }

    charge = gn.create_charge(body=body)

    params = {
        'id': charge['data']['charge_id']
    }

    try:
        response = gn.pay_charge(params=params, body=payment)
        print(response)

        # Pegando do corpo da resposta
        pdf_link = response['data']['pdf']['charge']
        barcode = response['data']['barcode']
        visualizar_pdf = response['data']['billet_link']

        # Armazenando os JSON's em um dicionário
        data = {
            'cliente_nome': payment['payment']['banking_billet']['customer']['name'],
            'cliente_email': payment['payment']['banking_billet']['customer']['email'],
            'cliente_cpf': payment['payment']['banking_billet']['customer']['cpf'],
            'cliente_cnpj': payment['payment']['banking_billet']['customer'].get('juridical_person', {}).get('cnpj', ''), # Se o CNPJ estiver disponível pegar, se não, str vazio
            'cliente_nome_pj': payment['payment']['banking_billet']['customer'].get('juridical_person', {}).get('corporate_name', ''),  # Se razão social estiver disponível pegar, se não, str vazio
            'data_expiracao': payment['payment']['banking_billet']['expire_at'],
            'valor_total': charge['data']['total'],
            'cobranca_id': charge['data']['charge_id'],
            'items': items,
            'shippings': shippings,
        }
        # Armazenando os dados do dicionário em uma variável session (armazenar temporariamente, sem ter que criar outra rota)
        session['boleto_dados'] = data

        return jsonify({"pdf_link": pdf_link,
                        "barcode": barcode,
                        "visualizar_pdf": visualizar_pdf,
                        "data": data}
                       )

    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/detalhar_cobranca/<int:charge_id>', methods=['GET'])
def detalharCobrançaPorId(charge_id):
    params = {
        'id': charge_id
    }

    response = gn.detail_charge(params=params)
    print(response)

    return jsonify({"response": response})

@app.route('/detalhar_pagamento/<int:payment_id>', methods=['GET'])
def detalharPagamentoPorId(payment_id):
    params = {
        'id': payment_id
    }

    response = gn.pay_detail_payment(params=params)
    print(response)

    return jsonify({"response": response})

@app.route('/detalhar_cobrancas/<data_inicio>/<data_fim>', methods=['GET'])
def detalharListaCobranças(data_inicio, data_fim):
    params = {
        'dataInicio': data_inicio,
        'dataFim': data_fim
    }

    response = gn.pay_list_payments(params=params)
    print(response)

    return jsonify({"response": response})


@app.route('/pagamentos/boleto', methods=['GET', 'POST'])
def pagamentoBoleto():
    # Pegando os dados armazenados na session
    boleto_dados = session.get('boleto_dados', {})

    return render_template('gerencianet/pagamento_boleto.html', data=boleto_dados, 
                           formatar_cpf=formatar_cpf, 
                           formatar_cnpj=formatar_cnpj, 
                           formatacao_valor_numerico=formatacao_valor_numerico,
                           formatar_apenas_data=formatar_apenas_data,
                           mapeamento_breadcrumbs=mapeamento_breadcrumbs)

@app.route('/pagamentos/cartao_credito', methods=['GET', 'POST'])
def pagamentoCartaoCredito():
    return render_template('gerencianet/pagamento_cartao_credito.html', mapeamento_breadcrumbs=mapeamento_breadcrumbs)
