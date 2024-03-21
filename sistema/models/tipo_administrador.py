from ..models.base_model import BaseModel, db


class TipoAdministrador (BaseModel):
    __tablename__ = 'tipo_administrador'
    tipo = db.Column(db.String(100), nullable=False)

    def __init__(self, tipo):
        self.tipo = tipo
