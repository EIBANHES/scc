# Tabela Andar

insert into condominio.andar (nome, id, data_criacao, data_alteracao, ativo) values 
('Andar 01', 1, NOW(), NOW(), 1 ),
('Andar 02', 2, NOW(), NOW(), 1 ),
('Andar 03', 3, NOW(), NOW(), 1 ),
('Andar 04', 4, NOW(), NOW(), 1 ),
('Andar 05', 5, NOW(), NOW(), 1 ),
('Andar 06', 6, NOW(), NOW(), 1 ),
('Andar 07', 7, NOW(), NOW(), 1 ),
('Andar 08', 8, NOW(), NOW(), 1 ),
('Andar 09', 9, NOW(), NOW(), 1 ),
('Andar 10', 10, NOW(), NOW(), 1 );

# Tabela tipo_morador

INSERT INTO condominio.tipo_morador (tipo,data_criacao,data_alteracao,ativo) VALUES
	 ('Proprietário: Cônjunge', NOW(), NOW(), 1),
	 ('Proprietário: Filho',NOW(), NOW(), 1),
	 ('Inquilino: Responsável',NOW(), NOW(), 1),
	 ('Inquilino: Cônjuge',NOW(), NOW(), 1),
	 ('Inquilino: Filho',NOW(), NOW(), 1),
	 ('Imobiliária',NOW(), NOW(), 1);

# Tabela tipo_administrador

INSERT INTO condominio.tipo_administrador (tipo,data_criacao,data_alteracao,ativo) VALUES
	 ('Síndico', NOW(), NOW(), 1),
	 ('Subsíndico', NOW(), NOW(), 1),
	 ('Gerente', NOW(), NOW(), 1);

# Tabela categoria_produto

INSERT INTO condominio.categoria_produto (tipo, data_criacao, data_alteracao, ativo) VALUES
    ('Parafusos', NOW(), NOW(), 1),
    ('Ferramentas', NOW(), NOW(), 1),
    ('Equipamentos de Segurança', NOW(), NOW(), 1),
    ('Materiais de Limpeza', NOW(), NOW(), 1),
    ('Embalagens', NOW(), NOW(), 1),
    ('Iluminação', NOW(), NOW(), 1),
    ('Eletrônicos', NOW(), NOW(), 1),
    ('Ferragens', NOW(), NOW(), 1),
    ('Material Elétrico', NOW(), NOW(), 1),
    ('Produtos Químicos', NOW(), NOW(), 1);
    
	# Tabela tipo_garagem
	INSERT INTO condominio.tipo_garagem  (tipo, data_criacao, data_alteracao, ativo) VALUES
    ('Subsolo 1', NOW(), NOW(), 1),
    ('Subsolo 2', NOW(), NOW(), 1);
    
   	# Tabela tipo_animal
   INSERT INTO condominio.tipo_animal  (tipo, data_criacao, data_alteracao, ativo) VALUES
    ('Cachorro', NOW(), NOW(), 1),
    ('Gato', NOW(), NOW(), 1),
   	('Cachorro e gato', NOW(), NOW(), 1),
    ('Pássaro', NOW(), NOW(), 1),
    ('Outros', NOW(), NOW(), 1);