from sistema import app,gn, flash
from sistema.utils.formata_data import formatar_data
from flask_login import current_user
import base64
import os


def criar_cobranca_pix():
    cpf_numerico = ''.join(filter(str.isdigit, current_user.cpf))

    body = {
        'calendario': {
            'expiracao': 3600
        },
        'devedor': {
            'cpf': cpf_numerico,
            'nome': current_user.nome
        },
        'valor': {
            'original': '0.01'
        },
        'chave': '47728c1f-5e22-48d8-b328-bb391ba61c06',
        'solicitacaoPagador': 'Cobrança dos serviços prestados.'
    }

    try:
        response = gn.response = gn.pix_create_immediate_charge(body=body)
        return response
    except:
        flash('Não foi possível realizar uma cobrança pix.', 'danger')
        return None

def cria_qrcode_pix(response, id_pix):
    params =  {'id': id_pix}
    response = gn.pix_generate_QRCode(params=params)

    if ('imagemQrcode' in response):
        qr_code_image = base64.b64decode(
            response['imagemQrcode'].replace('data:image/png;base64,', ''))
        save_path = os.path.join(
            app.root_path, "static", "imagens", "qrCodeImage.png")
        with open(save_path, "wb") as fh:
            fh.write(qr_code_image)

    return response['qrcode']
