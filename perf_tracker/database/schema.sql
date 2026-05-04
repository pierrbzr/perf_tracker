-- ============================================================
-- PERF TRACKER - Schéma Base de données
-- ============================================================
 
-- ============================================================
-- UTILISATEURS STAFF (Prépa / Coach)
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nom         TEXT NOT NULL,
    prenom      TEXT NOT NULL,
    role        TEXT NOT NULL CHECK (role IN ('prepa', 'coach')),
    email       TEXT NOT NULL UNIQUE,
    password    TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ============================================================
-- JOUEURS
-- ============================================================
CREATE TABLE IF NOT EXISTS players (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nom             TEXT NOT NULL,
    prenom          TEXT NOT NULL,
    numero          INTEGER,
    poste           TEXT,
    date_naissance  INTEGER,
    taille          INTEGER,
    poids           INTEGER,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ============================================================
-- WELLNESS 
-- Échelle : 0 à 5 pour chaque indicateur
-- ============================================================
CREATE TABLE IF NOT EXISTS wellness(
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id       INTEGER NOT NULL REFERENCES players(id),
    date            TEXT NOT NULL,
    sommeil         INTEGER NOT NULL CHECK(sommeil BETWEEN 0 AND 5),
    humeur          INTEGER NOT NULL CHECK(humeur BETWEEN 0 AND 5),
    energie         INTEGER NOT NULL CHECK(energie BETWEEN 0 AND 5),
    courbatures     INTEGER NOT NULL CHECK(courbatures BETWEEN 0 AND 5),
    stress          INTEGER NOT NULL CHECK(stress BETWEEN 0 AND 5),
    score_total     REAL,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(player_id, date)
);

-- ============================================================
-- RPE 
-- Échelle : 1 à 10
-- ============================================================
CREATE TABLE IF NOT EXISTS rpe (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id       INTEGER NOT NULL REFERENCES players(id),
    date            TEXT NOT NULL,
    rpem            INTEGER NOT NULL CHECK(rpem BETWEEN 0 AND 10),
    rpec            INTEGER NOT NULL CHECK(rpec BETWEEN 0 AND 10),
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(player_id, date)
);

-- ============================================================
-- INDEX pour accélérer les requêtes fréquentes
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_wellness_player_date ON wellness(player_id, date);
CREATE INDEX IF NOT EXISTS idx_rpe_player_date ON rpe(player_id, date);