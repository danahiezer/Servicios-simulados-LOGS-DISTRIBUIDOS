CREATE TABLE logs (
    id          SERIAL PRIMARY KEY,
    timestamp   TIMESTAMPTZ NOT NULL,
    received_at TIMESTAMPTZ DEFAULT NOW(),
    service     VARCHAR(100) NOT NULL,
    severity    VARCHAR(20) NOT NULL,
    message     TEXT NOT NULL
);

SELECT * FROM logs;