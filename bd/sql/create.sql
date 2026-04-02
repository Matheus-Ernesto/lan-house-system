-- Tabela: estado
CREATE TABLE IF NOT EXISTS estado (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_estado_nome ON estado(nome);

-- Tabela: cidade
CREATE TABLE IF NOT EXISTS cidade (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_cidade_nome ON cidade(nome);

-- Tabela: usuario
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    nome TEXT NOT NULL,
    telefone TEXT,
    cpf TEXT UNIQUE,
    localidadeEstado INTEGER,
    localidadeCidade INTEGER,
    bloqueado INTEGER DEFAULT 0,
    apagado INTEGER DEFAULT 0,
    FOREIGN KEY (localidadeEstado) REFERENCES estado(id) ON DELETE SET NULL,
    FOREIGN KEY (localidadeCidade) REFERENCES cidade(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_usuario_email ON usuario(email);
CREATE INDEX IF NOT EXISTS idx_usuario_cpf ON usuario(cpf);
CREATE INDEX IF NOT EXISTS idx_usuario_localidadeEstado ON usuario(localidadeEstado);
CREATE INDEX IF NOT EXISTS idx_usuario_localidadeCidade ON usuario(localidadeCidade);
CREATE INDEX IF NOT EXISTS idx_usuario_bloqueado ON usuario(bloqueado);
CREATE INDEX IF NOT EXISTS idx_usuario_apagado ON usuario(apagado);

-- Tabela: jogo
CREATE TABLE IF NOT EXISTS jogo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
);

CREATE INDEX IF NOT EXISTS idx_jogo_nome ON jogo(nome);

-- Tabela: lanHouse
CREATE TABLE IF NOT EXISTS lanHouse (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario INTEGER NOT NULL,
    endereco TEXT NOT NULL,
    telefone TEXT NOT NULL,
    foto1 TEXT,
    foto2 TEXT,
    foto3 TEXT,
    preco REAL NOT NULL,
    titulo TEXT NOT NULL,
    descricao TEXT,
    tipoPublico INTEGER NOT NULL CHECK (tipoPublico BETWEEN 0 AND 4),
    vagas INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (usuario) REFERENCES usuario(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_lanHouse_usuario ON lanHouse(usuario);
CREATE INDEX IF NOT EXISTS idx_lanHouse_tipoPublico ON lanHouse(tipoPublico);
CREATE INDEX IF NOT EXISTS idx_lanHouse_preco ON lanHouse(preco);

-- Tabela: campeonato
CREATE TABLE IF NOT EXISTS campeonato (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario INTEGER NOT NULL,
    endereco TEXT NOT NULL,
    telefone TEXT NOT NULL,
    jogo INTEGER NOT NULL,
    descricao TEXT,
    categoria INTEGER NOT NULL CHECK (categoria BETWEEN 0 AND 2),
    vagas INTEGER NOT NULL DEFAULT 0,
    timeAberto INTEGER DEFAULT 1,
    quantidadePorTime INTEGER DEFAULT 1,
    discord TEXT,
    outrasRedes TEXT,
    FOREIGN KEY (usuario) REFERENCES usuario(id) ON DELETE CASCADE,
    FOREIGN KEY (jogo) REFERENCES jogo(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_campeonato_usuario ON campeonato(usuario);
CREATE INDEX IF NOT EXISTS idx_campeonato_jogo ON campeonato(jogo);
CREATE INDEX IF NOT EXISTS idx_campeonato_categoria ON campeonato(categoria);
CREATE INDEX IF NOT EXISTS idx_campeonato_timeAberto ON campeonato(timeAberto);

-- Tabela: agendamento
CREATE TABLE IF NOT EXISTS agendamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario INTEGER NOT NULL,
    campeonato INTEGER NOT NULL,
    dataCriacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario) REFERENCES usuario(id) ON DELETE CASCADE,
    FOREIGN KEY (campeonato) REFERENCES campeonato(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_agendamento_usuario ON agendamento(usuario);
CREATE INDEX IF NOT EXISTS idx_agendamento_campeonato ON agendamento(campeonato);
CREATE INDEX IF NOT EXISTS idx_agendamento_dataCriacao ON agendamento(dataCriacao);