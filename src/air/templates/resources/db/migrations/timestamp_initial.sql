-- migrate:up
-- PostgreSQL table creation script for {{ name }}

CREATE TABLE {{ name }} (
    id SERIAL PRIMARY KEY,
    {%- for name,type in fields.items() %}
    {{ name }} {{ type }},
    {%- endfor %}
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- migrate:down
DROP TABLE IF EXISTS {{name}};
