CREATE TABLE IF NOT EXISTS animales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especie VARCHAR(100) NOT NULL,
    color VARCHAR(100),
    edad INT
);

INSERT INTO animales (nombre, especie, color, edad) VALUES
    ('Simba', 'León', 'Dorado', 5),
    ('Dumbo', 'Elefante', 'Gris', 10),
    ('Pingu', 'Pingüino', 'Negro y Blanco', 3);