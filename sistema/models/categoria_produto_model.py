from ..models.base_model import BaseModel, db


class CategoriaProduto(BaseModel):
    __tablename__ = 'categoria_produto'
    tipo = db.Column(db.String(100), nullable=False)
    # Relationship
    produtos = db.relationship(
        'Almoxarifado', back_populates='categoria', lazy=True)

    def __init__(self, tipo):
        self.tipo = tipo
