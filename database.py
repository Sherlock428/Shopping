from peewee import *
from playhouse.migrate import *

db = SqliteDatabase('Shopping.db')


class BaseModel(Model):
    class Meta:
        database = db

class Loja(BaseModel):
    Nome = CharField()
    Cnpj = CharField(unique=True)
    Senha = CharField()
    Faturamento = DecimalField(default=0)
    Bonus_tipo = TextField(null = True)
    Bonus_valor = TextField(null = True)


class Produto(BaseModel):
    Nome = CharField()
    Preco = DecimalField()
    Unidade = IntegerField()
    loja = ForeignKeyField(Loja, backref='produtos')
    


class Cliente(BaseModel):
    Nome = CharField()
    Email = CharField(unique=True)
    Senha = CharField()
    Credito = IntegerField()
    
class Bonus(BaseModel):
    cliente = ForeignKeyField(Cliente, backref='bonus')
    loja = ForeignKeyField(Loja, backref='bonus')
    Tipo = TextField(null = True)
    Valor = TextField(null = True)

class Cliente_produtos(BaseModel):
    cliente = ForeignKeyField(Cliente, backref='produtos')
    produto = ForeignKeyField(Produto, backref='clientes')
    quantidade = IntegerField()

def coluna_existe(nome_tabela, nome_coluna):
    cursor = db.execute_sql(f"PRAGMA table_info({nome_tabela});")
    colunas = cursor.fetchall()
    for coluna in colunas:
        if coluna[1] == nome_coluna:
            return True
    return False
def conectar_banco():
    db.connect()
    db.create_tables([Loja, Produto, Cliente, Bonus, Cliente_produtos])
    
    migrator = SqliteMigrator(db)

    if not coluna_existe('loja', 'Bonus_tipo'):
        add_bonus_tipo = migrator.add_column('loja', 'Bonus_tipo', TextField(null=True))
        migrate(add_bonus_tipo)
    if not coluna_existe('Loja', 'Bonus_valor'):
        add_bonus_valor = migrator.add_column('loja', 'Bonus_valor', TextField(null=True))
        migrate(add_bonus_valor)

    if not coluna_existe('Loja', 'Faturamento'):
        add_faturamento = migrator.add_column('loja', 'Faturamento', DecimalField(default=0))
        migrate(add_faturamento)

        update = Loja.update(Bonus_tipo='DefaultType', Bonus_valor='0', Faturamemento=0).execute()
        Loja.update(Faturamento=0.0).where(Loja.Faturamento >> None).execute()