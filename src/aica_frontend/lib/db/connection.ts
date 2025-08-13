import { Pool } from 'pg';

const pool = new Pool({
  user: process.env.POSTGRES_USER,
  host: process.env.POSTGRES_SERVER,
  database: process.env.POSTGRES_DB,
  password: process.env.POSTGRES_PASSWORD,
  port: parseInt(process.env.POSTGRES_PORT || '5432'),
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

export default pool;
