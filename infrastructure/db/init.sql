CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE customer_queries (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    embedding_id UUID NOT NULL,
    classification VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

   
);

--Sample data insertion
INSERT INTO customers (name, email) VALUES
('Ali Veli', 'ali@example.com'),
('Ayşe Fatma', 'ayse@example.com');

INSERT INTO customer_queries (customer_id, message, embedding_id, classification) VALUES
(1, 'I have an issue with my order.', '123e4567-e89b-12d3-a456-426614174000', 'complaint'),
(2, 'Can you help me with product information?', '123e4567-e89b-12d3-a456-426614174001', 'inquiry');