from ..models.base_model import BaseModel, db
from werkzeug.security import generate_password_hash, check_password_hash
from sistema import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.filter_by(id=user_id).first()


class Usuario (BaseModel, UserMixin):
    __tablename__ = 'usuario'
    nome = db.Column(db.String(100), nullable=False)
    razao_social = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(14), nullable=True)
    cnpj = db.Column(db.String(18), nullable=True)
    numero_contato = db.Column(db.String(15), nullable=False)
    tipo_administrador_id = db.Column(db.Integer, db.ForeignKey(
        'tipo_administrador.id'), nullable=False)
    senha = db.Column(db.String(120), nullable=False)

    tipo_administrador = db.relationship(
        'TipoAdministrador', backref='usuarios')

    def __init__(self, nome, razao_social, email, cpf, cnpj, numero_contato, tipo_administrador_id, senha):
        self.nome = nome
        self.razao_social = razao_social
        self.email = email
        self.cpf = cpf
        self.cnpj = cnpj
        self.numero_contato = numero_contato
        self.tipo_administrador_id = tipo_administrador_id
        self.senha = generate_password_hash(senha)

    def verificaSenha(self, pwd):
        return check_password_hash(self.senha, pwd)
