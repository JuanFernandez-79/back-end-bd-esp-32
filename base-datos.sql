CREATE DATABASE bdsensores;

CREATE TABLE lecturas_sensores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperatura FLOAT,
    humedad FLOAT,
    presion FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
