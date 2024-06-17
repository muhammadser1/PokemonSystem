CREATE DATABASE pokemon_db_1;

USE pokemon_db_1;

CREATE TABLE pokemons (
    id INT PRIMARY KEY NOT NULL,
    name VARCHAR(100) NOT NULL,
    height FLOAT NOT NULL,
    weight FLOAT NOT NULL
);

CREATE TABLE trainers (
    name VARCHAR(100) PRIMARY KEY NOT NULL,
    town VARCHAR(100) NOT NULL
);

CREATE TABLE types (
    name VARCHAR(100) PRIMARY KEY NOT NULL
);

CREATE TABLE teams (
    trainer_name VARCHAR(100),
    pokemon_id INT,
    PRIMARY KEY (trainer_name, pokemon_id),
    FOREIGN KEY (trainer_name) REFERENCES trainers(name) ON DELETE CASCADE,
    FOREIGN KEY (pokemon_id) REFERENCES pokemons(id) ON DELETE CASCADE
);

CREATE TABLE pokemon_types (
    type_name VARCHAR(100),
    pokemon_id INT,
    PRIMARY KEY (type_name, pokemon_id),
    FOREIGN KEY (type_name) REFERENCES types(name) ON DELETE CASCADE,
    FOREIGN KEY (pokemon_id) REFERENCES pokemons(id) ON DELETE CASCADE
);
