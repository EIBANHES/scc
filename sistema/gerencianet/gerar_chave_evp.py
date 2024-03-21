from gerencianet import Gerencianet

CREDENTIALS = {
    'client_id': 'Client_Id_d2a723ae6ecad7938d274319dae06ac9ec829264',
    'client_secret': 'Client_Secret_6297f19c3f00da27ec529aa6f4e20ac687d79cdd',
    'sandbox': False,
    'certificate': 'sistema/static/certificado.pem'
}

# Instancia gn
gn = Gerencianet(CREDENTIALS)

response =  gn.pix_create_evp()
print(response)