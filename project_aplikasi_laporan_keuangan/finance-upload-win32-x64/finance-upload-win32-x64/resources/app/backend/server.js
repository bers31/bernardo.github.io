require('dotenv').config();
console.log('SMTP Config loaded:', {
  host: process.env.SMTP_HOST,
  from: process.env.SMTP_FROM
});
const express = require('express');
const app = express();
const corsMiddleware = require('./middleware/cors');
const errorHandler = require('./middleware/errorHandler');
const jsonParser = require('./middleware/jsonParser');
const logger = require('./middleware/logger');
const verifyToken = require('./middleware/verifyToken');
const authRoutes = require('./routes/auth');

// Gunakan middleware
app.use(corsMiddleware);
app.use(jsonParser);
app.use(logger);

// Test route untuk mengecek server berjalan
app.get('/api/test', (req, res) => {
  res.json({ message: 'Server is running' });
});

// Rute autentikasi dengan prefix /api
app.use('/api', authRoutes);

// Rute publik yang tidak memerlukan autentikasi
app.get('/api/public', (req, res) => {
  res.json({ message: 'Ini adalah rute publik' });
});

// Rute yang dilindungi yang memerlukan autentikasi
app.get('/api/protected', verifyToken, (req, res) => {
  res.json({ message: 'Ini adalah rute yang dilindungi', user: req.user });
});

// Middleware untuk menangani kesalahan
app.use(errorHandler);

// Handle 404
app.use((req, res) => {
  res.status(404).json({ message: 'Route tidak ditemukan' });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server berjalan di port ${PORT}`);
  console.log(`Test server di http://localhost:${PORT}/api/test`);
});

// Handle uncaught errors
process.on('unhandledRejection', (err) => {
  console.error('Unhandled Rejection:', err);
});