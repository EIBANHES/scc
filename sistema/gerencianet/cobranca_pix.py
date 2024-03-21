from gerencianet import Gerencianet
import base64


body = {
    'calendario': {
        'expiracao': 3600
    },
    'devedor': {
        'cpf': '04559174180',
        'nome': 'Emanuel B Ibanhes'
    },
    'valor': {
        'original': '0.01'
    },
    'chave': '4c1aff23-5961-4ee7-a2d3-94eee8fe2af9',
    'solicitacaoPagador': 'Cobrança dos serviços prestados.'
}

response =  gn.pix_create_immediate_charge(body=body)

params = {
    'id': response['loc']['id']
}

response =  gn.pix_generate_QRCode(params=params)
print(response)

#Generate QRCode Image
if('imagemQrcode' in response):
    with open("qrCodeImage.png", "wb") as fh:
        fh.write(base64.b64decode(response['imagemQrcode'].replace('data:image/png;base64,', '')))