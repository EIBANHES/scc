from sistema import db
from datetime import datetime
import pytz

fuso_horario = pytz.timezone('America/Sao_Paulo')


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, autoincrement=True,
                   nullable=False, primary_key=True)

    data_criacao = db.Column(
        db.DateTime, default=lambda: datetime.now(fuso_horario), nullable=False
    )

    data_alteracao = db.Column(
        db.DateTime, default=lambda: datetime.now(fuso_horario),
        onupdate=lambda: datetime.now(fuso_horario), nullable=False
    )

    ativo = db.Column(db.Boolean, default=True, nullable=False)
