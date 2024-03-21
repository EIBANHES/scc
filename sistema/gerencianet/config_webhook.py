from gerencianet import Gerencianet

CREDENTIALS = {
    'client_id': 'Client_Id_800df4436357faa453b8e1fa35b97dfbb4dda251',
    'client_secret': 'Client_Secret_5fb7b5671429b1c251f046ae5167c090502ff4f0',
    'sandbox': False,
    'certificate': 'sistema/static/certificado-producao.pem'
}

# Instancia gn
gn = Gerencianet(CREDENTIALS)

headers = {
    'x-skip-mtls-checking': 'true'
}

params = {
    'chave': '47728c1f-5e22-48d8-b328-bb391ba61c06'
}

body = {
    'webhookUrl': 'https://webhook.site/3f9283de-265d-4cd6-b1f1-0c9f59fd7e8c'
}

response =  gn.pix_config_webhook(params=params, body=body, headers=headers)
print(response)