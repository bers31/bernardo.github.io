const mysql = require('mysql2/promise');
const fs = require('fs');
const path = require('path');

async function setupDatabase() {
  try {
    // Baca konfigurasi dari .env
    require('dotenv').config();

    const connection = await mysql.createConnection({
      host: process.env.DB_HOST,
      user: process.env.DB_USER,
      password: process.env.DB_PASSWORD
    });

    // Buat database jika belum ada
    await connection.query(`CREATE DATABASE IF NOT EXISTS ${process.env.DB_NAME}`);
    
    // Jalankan migrasi Prisma
    const { exec } = require('child_process');
    exec('npx prisma migrate deploy', (error, stdout, stderr) => {
      if (error) {
        console.error(`Migration error: ${error}`);
        return;
      }
      console.log(`Database setup complete: ${stdout}`);
    });

  } catch (error) {
    console.error('Database setup failed:', error);
  }
}

setupDatabase();