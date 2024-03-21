from ..models.base_model import BaseModel, db


class TipoGaragem (BaseModel):
    __tablename__ = 'tipo_garagem'
    tipo = db.Column(db.String(100), nullable=False)

    def __init__(self, tipo):
        self.tipo = tipo
