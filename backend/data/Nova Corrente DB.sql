CREATE DATABASE IF NOT EXISTS STOCK;
USE STOCK; 

CREATE TABLE Usuario (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    nome_usuario VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Familia (
    familia_id INT AUTO_INCREMENT PRIMARY KEY,
    nome_familia VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Fornecedor (
    fornecedor_id INT AUTO_INCREMENT PRIMARY KEY,
    nome_fornecedor VARCHAR(255) NOT NULL UNIQUE,
    contato_email VARCHAR(100),
    contato_telefone VARCHAR(20)
);

CREATE TABLE Material (
    material_id INT AUTO_INCREMENT PRIMARY KEY,
    nome_material VARCHAR(255) NOT NULL,
    descricao TEXT,
    familia_id INT, 
    quantidade_atual INT NOT NULL DEFAULT 0,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (familia_id) REFERENCES Familia(familia_id)
);

CREATE TABLE Fornecedor_Material (
    fornecedor_id INT,
    material_id INT,
    
    FOREIGN KEY (fornecedor_id) REFERENCES Fornecedor(fornecedor_id),
    FOREIGN KEY (material_id) REFERENCES Material(material_id),
    
    PRIMARY KEY (fornecedor_id, material_id)
);

CREATE TABLE MovimentacaoEstoque (
    movimentacao_id INT AUTO_INCREMENT PRIMARY KEY,
    material_id INT,
    usuario_id INT,
    tipo_movimentacao ENUM('ENTRADA', 'SAIDA') NOT NULL, 
    quantidade_movimentada INT NOT NULL,
    data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (material_id) REFERENCES Material(material_id),
    FOREIGN KEY (usuario_id) REFERENCES Usuario(usuario_id)
);

DELIMITER $$
CREATE TRIGGER trg_aumentar_estoque
AFTER INSERT ON MovimentacaoEstoque
FOR EACH ROW
BEGIN
    IF NEW.tipo_movimentacao = 'ENTRADA' THEN
        UPDATE Material
        SET quantidade_atual = quantidade_atual + NEW.quantidade_movimentada
        WHERE material_id = NEW.material_id;
    END IF;
END$$

CREATE TRIGGER trg_diminuir_estoque
AFTER INSERT ON MovimentacaoEstoque
FOR EACH ROW
BEGIN
    IF NEW.tipo_movimentacao = 'SAIDA' THEN
        UPDATE Material
        SET quantidade_atual = quantidade_atual - NEW.quantidade_movimentada
        WHERE material_id = NEW.material_id;
    END IF;
END$$
DELIMITER ;