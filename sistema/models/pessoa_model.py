from ..models.base_model import BaseModel, db


class Pessoa (BaseModel):
    __tablename__ = 'pessoa'
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    rg = db.Column(db.String(9), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    profissao = db.Column(db.String(50), nullable=True)
    numero_principal = db.Column(db.String(15), nullable=False)
    numero_secundario = db.Column(db.String(15), nullable=True)
    tipo_morador_id = db.Column(
        db.Integer, db.ForeignKey('tipo_morador.id'), nullable=True)

    # atributo pessoas na classe TipoMorador permite acessar todas as pessoas associadas a um tipo de morador específico.
    tipo_morador = db.relationship(
        'TipoMorador', backref='pessoas_tipo', lazy=True)
    # atributo pessoa na classe Imovel permite acessar todas as pessoas associadas a um Imovel específico.
    imoveis = db.relationship('Imovel', backref='pessoa_imovel', lazy=True)

    def __init__(
        self, nome, email, cpf, rg, data_nascimento, profissao, numero_principal, numero_secundario,
        tipo_morador_id
    ):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.rg = rg
        self.data_nascimento = data_nascimento
        self.profissao = profissao
        self.numero_principal = numero_principal
        self.numero_secundario = numero_secundario
        self.tipo_morador_id = tipo_morador_id
