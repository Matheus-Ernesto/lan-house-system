-- Insert de estados
INSERT INTO estado (nome) VALUES 
('São Paulo'),
('Rio de Janeiro'),
('Minas Gerais'),
('Rio Grande do Sul'),
('Paraná'),
('Bahia'),
('Santa Catarina'),
('Pernambuco'),
('Ceará'),
('Goiás');

-- Insert de cidades
INSERT INTO cidade (nome) VALUES 
('São Paulo'),
('Rio de Janeiro'),
('Belo Horizonte'),
('Porto Alegre'),
('Curitiba'),
('Salvador'),
('Florianópolis'),
('Recife'),
('Fortaleza'),
('Goiânia'),
('Campinas'),
('Niterói'),
('Joinville'),
('Caxias do Sul'),
('Londrina');

-- Insert de jogos
INSERT INTO jogo (nome) VALUES 
('League of Legends'),
('Counter-Strike 2'),
('Valorant'),
('Dota 2'),
('Free Fire'),
('Fortnite'),
('Call of Duty'),
('FIFA 25'),
('Minecraft'),
('Rocket League');

-- Insert de usuarios
INSERT INTO usuario (email, senha, nome, telefone, cpf, localidadeEstado, localidadeCidade, bloqueado, apagado) VALUES 
('joao.silva@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkKeYF5ZEhLpUZqXqXqXqXqXqXqXqXqXq', 'João Silva', '(11) 99999-1111', '111.111.111-11', 1, 1, 0, 0),
('maria.santos@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkKeYF5ZEhLpUZqXqXqXqXqXqXqXqXq', 'Maria Santos', '(11) 99999-2222', '222.222.222-22', 1, 1, 0, 0),
('pedro.oliveira@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkKeYF5ZEhLpUZqXqXqXqXqXqXqXqXq', 'Pedro Oliveira', '(21) 99999-3333', '333.333.333-33', 2, 2, 0, 0),
('ana.pereira@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkKeYF5ZEhLpUZqXqXqXqXqXqXqXqXq', 'Ana Pereira', '(31) 99999-4444', '444.444.444-44', 3, 3, 0, 0),
('carlos.rocha@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkKeYF5ZEhLpUZqXqXqXqXqXqXqXqXq', 'Carlos Rocha', '(41) 99999-5555', '555.555.555-55', 4, 4, 0, 0),
('fernanda.lima@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkKeYF5ZEhLpUZqXqXqXqXqXqXqXqXq', 'Fernanda Lima', '(51) 99999-6666', '666.666.666-66', 5, 5, 0, 0),
('rafael.alves@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkKeYF5ZEhLpUZqXqXqXqXqXqXqXqXq', 'Rafael Alves', '(71) 99999-7777', '777.777.777-77', 6, 6, 0, 0),
('patricia.souza@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkKeYF5ZEhLpUZqXqXqXqXqXqXqXqXq', 'Patricia Souza', '(47) 99999-8888', '888.888.888-88', 7, 7, 0, 0),
('lucas.rodrigues@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkKeYF5ZEhLpUZqXqXqXqXqXqXqXqXq', 'Lucas Rodrigues', '(81) 99999-9999', '999.999.999-99', 8, 8, 0, 0),
('amanda.costa@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkKeYF5ZEhLpUZqXqXqXqXqXqXqXqXq', 'Amanda Costa', '(85) 99999-0000', '000.000.000-00', 9, 9, 0, 0);

-- Insert de lanHouses
INSERT INTO lanHouse (usuario, endereco, telefone, foto1, foto2, foto3, preco, titulo, descricao, tipoPublico, vagas) VALUES 
(1, 'Av. Paulista, 1000 - São Paulo/SP', '(11) 3000-1000', 'assets/1.jpg', 'https://example.com/foto2.jpg', 'https://example.com/foto3.jpg', 12.90, 'Gamer Station Paulista', 'A melhor lan house da Av. Paulista com PCs gamers de última geração', 3, 25),
(2, 'Rua Augusta, 500 - São Paulo/SP', '(11) 3000-2000', 'assets/2.jpg', 'https://example.com/foto2.jpg', NULL, 10.50, 'Augusta Game Center', 'Ambiente gamer com 30 estações e clima descontraído', 2, 30),
(3, 'Av. Atlântica, 2000 - Rio de Janeiro/RJ', '(21) 3000-3000', 'assets/3.jpg', NULL, NULL, 15.00, 'Cyber Copacabana', 'Lan house com vista para o mar e PCs potentes', 4, 20),
(4, 'Rua da Bahia, 1500 - Belo Horizonte/MG', '(31) 3000-4000', 'assets/4.jpg', 'https://example.com/foto2.jpg', 'https://example.com/foto3.jpg', 8.90, 'BH Game House', 'O melhor custo-benefício de Belo Horizonte', 1, 40),
(5, 'Av. Ipiranga, 300 - Porto Alegre/RS', '(51) 3000-5000', 'assets/5.jpg', 'https://example.com/foto2.jpg', NULL, 11.50, 'Gamer Sul', 'Especializada em campeonatos de CS2 e Valorant', 3, 35);

-- Insert de campeonatos
INSERT INTO campeonato (usuario, endereco, telefone, jogo, descricao, categoria, vagas, timeAberto, quantidadePorTime, discord, outrasRedes) VALUES 
(1, 'Av. Paulista, 1000 - São Paulo/SP', '(11) 3000-1000', 1, 'Campeonato de League of Legends - 5x5 - Prêmio de R$ 5.000', 2, 16, 1, 5, 'https://discord.gg/gamerstation', 'https://instagram.com/gamerstation'),
(2, 'Rua Augusta, 500 - São Paulo/SP', '(11) 3000-2000', 2, 'Torneio de CS2 2x2 - Inscrição grátis', 1, 32, 0, 2, 'https://discord.gg/augustagame', 'https://twitch.tv/augustagame'),
(3, 'Av. Atlântica, 2000 - Rio de Janeiro/RJ', '(21) 3000-3000', 3, 'Competição de Valorant - Ranking e premiação', 2, 20, 1, 5, 'https://discord.gg/cybercopacabana', 'https://twitter.com/cybercopacabana'),
(1, 'Av. Paulista, 1000 - São Paulo/SP', '(11) 3000-1000', 4, 'Dota 2 Tournament - 5x5 - 8 times', 2, 40, 1, 5, 'https://discord.gg/gamerstation', 'https://youtube.com/gamerstation'),
(4, 'Rua da Bahia, 1500 - Belo Horizonte/MG', '(31) 3000-4000', 5, 'Free Fire Solo - 100 vagas - Participe!', 0, 100, 0, 1, 'https://discord.gg/bhgamehouse', 'https://facebook.com/bhgamehouse'),
(5, 'Av. Ipiranga, 300 - Porto Alegre/RS', '(51) 3000-5000', 2, 'CS2 Championship - 5x5 - Inscrições abertas', 2, 80, 1, 5, 'https://discord.gg/gamersul', 'https://instagram.com/gamersul'),
(6, 'Av. Sete de Setembro, 500 - Salvador/BA', '(71) 3000-6000', 6, 'Fortnite Festival - 50 duplas', 1, 100, 0, 2, 'https://discord.gg/fortniteba', 'https://twitch.tv/fortniteba'),
(7, 'Av. Beira Mar, 300 - Florianópolis/SC', '(48) 3000-7000', 7, 'Call of Duty Tournament - 4x4', 2, 64, 1, 4, 'https://discord.gg/codfloripa', 'https://instagram.com/codfloripa');

-- Insert de agendamentos
INSERT INTO agendamento (usuario, campeonato, dataCriacao) VALUES 
(1, 1, datetime('now', '-5 days')),
(2, 1, datetime('now', '-4 days')),
(3, 1, datetime('now', '-3 days')),
(4, 2, datetime('now', '-2 days')),
(5, 2, datetime('now', '-1 days')),
(6, 3, datetime('now')),
(7, 3, datetime('now')),
(8, 4, datetime('now')),
(9, 5, datetime('now', '+1 day')),
(10, 5, datetime('now', '+1 day')),
(1, 6, datetime('now', '+2 days')),
(2, 7, datetime('now', '+3 days')),
(3, 8, datetime('now', '+4 days'));