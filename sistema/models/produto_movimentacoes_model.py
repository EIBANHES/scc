from ..models.base_model import BaseModel, db

class ProdutoMovimentacoes(BaseModel):
    __tablename__ = 'produto_movimentacoes'
    responsavel = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)
    quantidade_movimentada = db.Column(db.Float, nullable=False)
    quantidade_estoque = db.Column(db.Float, nullable=False)
    valor_unitario = db.Column(db.Float, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('almoxarifado.id'), nullable=False)

    def __init__(self, responsavel, tipo, quantidade_movimentada, quantidade_estoque, valor_unitario, valor_total, produto_id):
        self.responsavel = responsavel
        self.tipo = tipo
        self.quantidade_movimentada = quantidade_movimentada
        self.quantidade_estoque = quantidade_estoque
        self.valor_unitario = valor_unitario
        self.valor_total = valor_total
        self.produto_id = produto_id