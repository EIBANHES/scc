from ..models.base_model import BaseModel, db


class Morador (BaseModel):
    __tablename__ = 'morador'
    pessoa_id = db.Column(db.Integer, db.ForeignKey(
        'pessoa.id'), nullable=False)
    tipo_morador_id = db.Column(db.Integer, db.ForeignKey(
        'tipo_morador.id'), nullable=False)
    imovel_id = db.Column(db.Integer, db.ForeignKey(
        'imovel.id'), nullable=False)
    
    #Cria um atributo moradores na tabela Pessoa, para pegar moradores relacionados a uma pessoa
    pessoa = db.relationship('Pessoa', backref='moradores', lazy=True)
    #Cria um atributo moradores na tabela TipoMorador, para pegar moradores relacionados a um tipo especifico
    tipo_morador = db.relationship('TipoMorador', backref='morador_tipo', lazy=True)
    #Cria um atributo moradores na tabela Imovel, para pegar moradores relacionados a um imovel especifico
    imovel = db.relationship('Imovel', backref='morador_imovel', lazy=True)

    def __init__(self, pessoa_id, tipo_morador_id, imovel_id):
        self.pessoa_id = pessoa_id
        self.tipo_morador_id = tipo_morador_id
        self.imovel_id = imovel_id
