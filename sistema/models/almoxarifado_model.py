from ..models.base_model import BaseModel, db


class Almoxarifado(BaseModel):
    __tablename__ = 'almoxarifado'
    nome = db.Column(db.String(100), nullable=False)
    codigo_produto = db.Column(db.Integer, nullable=False)
    codigo_barras = db.Column(db.Integer, nullable=True)
    categoria_produto_id = db.Column(db.Integer, db.ForeignKey(
        'categoria_produto.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    quantidade_estoque = db.Column(db.Float, nullable=False)
    valor_total = db.Column(db.Float, nullable=True)
    # Relationship com categoria produto
    categoria = db.relationship(
        'CategoriaProduto', back_populates='produtos', lazy=True)
    # Relationship com movimentações
    movimentacoes = db.relationship('ProdutoMovimentacoes', backref='almoxarifado', lazy=True)


    def __init__(self, nome, codigo_produto, codigo_barras, categoria_produto_id, valor, quantidade_estoque, valor_total):
        self.nome = nome
        self.codigo_produto = codigo_produto
        self.codigo_barras = codigo_barras
        self.categoria_produto_id = categoria_produto_id
        self.valor = valor
        self.quantidade_estoque = quantidade_estoque
        self.valor_total = valor_total

    @property
    def total_movimentacoes(self):
        total_entrada = sum(m.quantidade_movimentada for m in self.movimentacoes if m.tipo == 'Entrada')
        total_saida = sum(m.quantidade_movimentada for m in self.movimentacoes if m.tipo == 'Saída')
        return total_entrada, total_saida
