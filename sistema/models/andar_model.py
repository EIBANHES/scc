from ..models.base_model import BaseModel, db

class Andar (BaseModel):
    __tablename__ = 'andar'
    nome = db.Column(db.String(20), nullable=False)

    def __init__(self, nome):
        self.nome = nome
        