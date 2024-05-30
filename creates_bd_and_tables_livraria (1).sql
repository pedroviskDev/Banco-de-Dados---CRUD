CREATE DATABASE db_livraria;

USE db_livraria;

CREATE TABLE IF NOT EXISTS Autor (
	cod_autor SMALLINT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    data_nasc DATE NOT NULL,
    pais_nasc VARCHAR(100) NOT NULL,
    biografia VARCHAR(300) NOT NULL
);

CREATE TABLE IF NOT EXISTS Livro (
	cod_livro SMALLINT AUTO_INCREMENT PRIMARY KEY, 
    nome VARCHAR(255) NOT NULL,
    lingua VARCHAR(45) NOT NULL,
    ano YEAR NOT NULL
);

CREATE TABLE IF NOT EXISTS Autor_has_Livro (
	cod_autor SMALLINT NOT NULL, 
    cod_livro SMALLINT NOT NULL,
    FOREIGN KEY (cod_autor) REFERENCES Autor(cod_autor),
    FOREIGN KEY (cod_livro) REFERENCES Livro(cod_livro)
);

CREATE TABLE IF NOT EXISTS Editora (
	cod_editora SMALLINT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(45) NOT NULL,
    endereco VARCHAR(255) NOT NULL,
    telefone VARCHAR(55) NOT NULL
);

CREATE TABLE IF NOT EXISTS Edicao (
	cod_isbn VARCHAR(55) PRIMARY KEY,
    preco DECIMAL NOT NULL,
    ano YEAR NOT NULL,
    num_pag INT NOT NULL,
    qtde_estoque INT NOT NULL,
    cod_livro SMALLINT NOT NULL,
    cod_editora SMALLINT NOT NULL,
    FOREIGN KEY (cod_livro) REFERENCES Livro(cod_livro),
    FOREIGN KEY (cod_editora) REFERENCES Editora(cod_editora)
);

# Criação da VIEW para
/*
VIEW - Todas as informações relacionadas aos livros com maior 
quantidade de edições em estoque atualmente - mostrando nome da editora, id da edição, 
título de livro e quantidade em estoque.
*/

CREATE VIEW view_livro_info AS
SELECT Editora.nome AS Nome_Editora, Edicao.cod_isbn AS ID_Edicao, Livro.nome AS Titulo_Livro, Edicao.qtde_estoque AS Quantidade_Estoque
FROM Livro
JOIN Edicao ON Livro.cod_livro = Edicao.cod_livro
JOIN Editora ON Edicao.cod_editora = Editora.cod_editora
WHERE Edicao.qtde_estoque = (
	SELECT MAX(qtde_estoque)
    FROM Edicao
);

SELECT * FROM view_livro_info;

# Criação dos Índices

CREATE INDEX index_nome_autor ON Autor(nome);
CREATE INDEX index_nome_livro ON Livro(nome);
CREATE INDEX index_nome_editora ON Editora(nome);


