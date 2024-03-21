from ..models.base_model import BaseModel, db


class TipoMorador (BaseModel):
    __tablename__ = 'tipo_morador'
    tipo = db.Column(db.String(100), nullable=False)

    def __init__ (self, tipo):
        self.tipo = tipo
