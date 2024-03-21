from gerencianet import Gerencianet

CREDENTIALS = {
    'client_id': 'Client_Id_800df4436357faa453b8e1fa35b97dfbb4dda251',
    'client_secret': 'Client_Secret_5fb7b5671429b1c251f046ae5167c090502ff4f0',
    'sandbox': False,
    'certificate': 'sistema/static/certificado-producao.pem'
}

# Instancia gn
gn = Gerencianet(CREDENTIALS)

params = {
    'txid': '17d1f116b43845828d61308b70b00a9c'
}

response =  gn.pix_detail_charge(params=params)
print(response)