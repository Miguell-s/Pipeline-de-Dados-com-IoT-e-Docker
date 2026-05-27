-- View 1: Média de temperatura por dispositivo
CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT
    room_id AS dispositivo,
    COUNT(*) AS total_leituras,
    AVG(temp) AS temperatura_media,
    MIN(temp) AS temperatura_minima,
    MAX(temp) AS temperatura_maxima
FROM
    temperature_readings
GROUP BY
    room_id
ORDER BY
    temperatura_media DESC;


-- View 2: Quantidade de leituras por hora
CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT
    EXTRACT(HOUR FROM noted_date) AS hora,
    COUNT(*) AS total_leituras
FROM
    temperature_readings
GROUP BY
    EXTRACT(HOUR FROM noted_date)
ORDER BY
    hora;


-- View 3: Temperatura máxima e mínima por dia
CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT
    DATE(noted_date) AS data,
    MIN(temp) AS temperatura_minima,
    MAX(temp) AS temperatura_maxima,
    AVG(temp) AS temperatura_media
FROM
    temperature_readings
GROUP BY
    DATE(noted_date)
ORDER BY
    data;
