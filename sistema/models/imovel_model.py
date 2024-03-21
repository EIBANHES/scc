from ..models.base_model import BaseModel, db


class Imovel(BaseModel):
    __tablename__ = 'imovel'
    andar_id = db.Column(db.Integer, db.ForeignKey('andar.id'), nullable=False)
    apartamento = db.Column(db.String(50), nullable=False)
    possui_pet = db.Column(db.Boolean, nullable=False)
    tipo_animal_id = db.Column(db.Integer, db.ForeignKey(
        'tipo_animal.id'), nullable=True)
    pessoa_id = db.Column(
        db.Integer, db.ForeignKey('pessoa.id'), nullable=True)
    andar_garagem = db.Column(db.Integer, db.ForeignKey(
        'tipo_garagem.id'), nullable=True)
    numero_garagem = db.Column(db.String(50), nullable=True)

    # Relationship para a tabela Andar
    andar = db.relationship('Andar', backref='imovel', lazy=True)
    tipo_animal = db.relationship('TipoAnimal', backref='animal', lazy=True)

    def __init__(self, andar_id, apartamento, possui_pet, tipo_animal_id, pessoa_id, numero_garagem, andar_garagem):
        self.andar_id = andar_id
        self.apartamento = apartamento
        self.possui_pet = possui_pet
        self.tipo_animal_id = tipo_animal_id
        self.pessoa_id = pessoa_id
        self.numero_garagem = numero_garagem
        self.andar_garagem = andar_garagem

