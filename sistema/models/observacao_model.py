from ..models.base_model import BaseModel, db


class Observacao(BaseModel):
    __tablename__ = 'observacao'
    descricao = db.Column(db.String(255), nullable=False)
    possui_imovel_vinculado = db.Column(db.Boolean, nullable=False)
    imovel_id = db.Column(
        db.Integer, db.ForeignKey('imovel.id'), nullable=True)

    # Relationship
    imoveis = db.relationship('Imovel', backref='observacoes', lazy=True)


def __init__(self, possui_imovel_vinculado, descricao, imovel_id):
    self.possui_imovel_vinculado = possui_imovel_vinculado
    self.descricao = descricao
    self.imovel_id = imovel_id
