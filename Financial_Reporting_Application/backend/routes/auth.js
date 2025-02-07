/* routes/auth.js */
const express = require('express');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const router = express.Router();
const pool = require('../config/database');
const { saveToDatabase, saveMonthlyTable } = require('../savetodatabase');
const { sendResetEmail } = require('../config/emailConfig');

// Tambahkan middleware autentikasi
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ message: 'Token tidak ditemukan' });
  }

  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) {
      return res.status(403).json({ message: 'Token tidak valid' });
    }
    req.user = user;
    next();
  });
};

// Endpoint untuk mengambil daftar users
router.get('/users', authenticateToken, async (req, res) => {
  try {
    // Mengambil data users dari database, kecuali password
    const [users] = await pool.execute(
      'SELECT id, username, email, roles, created_at FROM users'
    );
    
    console.log('Fetched users:', users); // Untuk debugging
    
    // Mengembalikan array users
    res.json(users);
  } catch (err) {
    console.error('Error fetching users:', err);
    res.status(500).json({ 
      message: 'Terjadi kesalahan server',
      detail: process.env.NODE_ENV === 'development' ? err.message : undefined 
    });
  }
});

// Endpoint Create User (POST)
router.post('/users', authenticateToken, async (req, res) => {
  const { username, email, roles, password } = req.body;
  
  try {
    // Validasi input
    if (!username || !email || !roles || !password) {
      return res.status(400).json({ message: 'Semua field harus diisi' });
    }

    // Check existing user
    const [existingUser] = await pool.execute(
      'SELECT * FROM users WHERE username = ? OR email = ?',
      [username, email]
    );

    if (existingUser.length > 0) {
      return res.status(400).json({ message: 'Username atau email sudah digunakan' });
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Insert new user
    const [result] = await pool.execute(
      'INSERT INTO users (username, email, roles, password) VALUES (?, ?, ?, ?)',
      [username, email, roles, hashedPassword]
    );

    res.status(201).json({
      message: 'User berhasil dibuat',
      user: {
        id: result.insertId,
        username,
        email,
        roles
      }
    });

  } catch (err) {
    console.error('Error creating user:', err);
    res.status(500).json({ message: 'Terjadi kesalahan server' });
  }
});

// Endpoint Update User (PUT)
router.put('/users/:id', authenticateToken, async (req, res) => {
  const { id } = req.params;
  const { username, email, roles, password } = req.body;

  try {
    // Check if user exists
    const [existingUser] = await pool.execute(
      'SELECT * FROM users WHERE id = ?',
      [id]
    );

    if (existingUser.length === 0) {
      return res.status(404).json({ message: 'User tidak ditemukan' });
    }

    // Check email/username uniqueness (excluding current user)
    const [duplicateCheck] = await pool.execute(
      'SELECT * FROM users WHERE (username = ? OR email = ?) AND id != ?',
      [username, email, id]
    );

    if (duplicateCheck.length > 0) {
      return res.status(400).json({ message: 'Username atau email sudah digunakan' });
    }

    let query = 'UPDATE users SET username = ?, email = ?, roles = ?';
    let params = [username, email, roles];

    // If password is provided, update it too
    if (password) {
      const hashedPassword = await bcrypt.hash(password, 10);
      query += ', password = ?';
      params.push(hashedPassword);
    }

    query += ' WHERE id = ?';
    params.push(id);

    await pool.execute(query, params);

    res.json({ 
      message: 'User berhasil diupdate',
      user: {
        id,
        username,
        email,
        roles
      }
    });

  } catch (err) {
    console.error('Error updating user:', err);
    res.status(500).json({ message: 'Terjadi kesalahan server' });
  }
});

// Endpoint Delete User (DELETE)
router.delete('/users/:id', authenticateToken, async (req, res) => {
  const { id } = req.params;

  try {
    // Check if user exists
    const [existingUser] = await pool.execute(
      'SELECT * FROM users WHERE id = ?',
      [id]
    );

    if (existingUser.length === 0) {
      return res.status(404).json({ message: 'User tidak ditemukan' });
    }

    // Delete the user
    await pool.execute(
      'DELETE FROM users WHERE id = ?',
      [id]
    );

    res.json({ 
      message: 'User berhasil dihapus',
      deletedUserId: id
    });

  } catch (err) {
    console.error('Error deleting user:', err);
    res.status(500).json({ message: 'Terjadi kesalahan server' });
  }
});

// Login endpoint dengan debugging
router.post('/login', async (req, res) => {
  const { username, password } = req.body;
  
  try {
    console.log('Login attempt for username:', username);

    // Check database connection
    await pool.getConnection().then(conn => {
      console.log('Database connection successful');
      conn.release();
    });

    // Query user
    const [users] = await pool.execute(
      'SELECT * FROM users WHERE username = ?',
      [username]
    );
    console.log('Query result length:', users.length);

    if (users.length === 0) {
      console.log('User not found');
      return res.status(401).json({ 
        message: 'Username atau password salah',
        attemptsLeft: 5
      });
    }

    const user = users[0];
    console.log('User found:', { 
      id: user.id, 
      username: user.username,
      hasPassword: !!user.password
    });

    // Check lock status
    if (user.locked_until && new Date(user.locked_until) > new Date()) {
      const timeLeft = Math.ceil((new Date(user.locked_until) - new Date()) / 1000);
      console.log('Account is locked for', timeLeft, 'seconds');
      return res.status(401).json({
        message: 'Akun terkunci',
        lockTimeLeft: timeLeft
      });
    }

    // Check reset requirement
    if (user.require_reset) {
      console.log('Password reset required');
      return res.status(401).json({
        message: 'Anda harus mereset password',
        requiresReset: true
      });
    }

    // Verify password
    try {
      const isValid = await bcrypt.compare(password, user.password);
      console.log('Password verification result:', isValid);

      if (!isValid) {
        const newAttempts = user.failed_attempts + 1;
        console.log('Failed attempt:', newAttempts);

        let updateQuery = 'UPDATE users SET failed_attempts = ? WHERE id = ?';
        let updateParams = [newAttempts, user.id];

        if (newAttempts >= 10) {
          updateQuery = 'UPDATE users SET failed_attempts = ?, require_reset = 1 WHERE id = ?';
          console.log('Too many attempts, requiring reset');
        } else if (newAttempts >= 5) {
          const lockUntil = new Date(Date.now() + 60000);
          updateQuery = 'UPDATE users SET failed_attempts = ?, locked_until = ? WHERE id = ?';
          updateParams = [newAttempts, lockUntil, user.id];
          console.log('Locking account until:', lockUntil);
        }

        await pool.execute(updateQuery, updateParams);

        return res.status(401).json({
          message: 'Username atau password salah',
          attemptsLeft: 10 - newAttempts
        });
      }
    } catch (bcryptError) {
      console.error('Bcrypt comparison error:', bcryptError);
      throw bcryptError;
    }

    // Reset failed attempts on successful login
    console.log('Login successful, resetting failed attempts');
    await pool.execute(
      'UPDATE users SET failed_attempts = 0, locked_until = NULL WHERE id = ?',
      [user.id]
    );

    // Di auth.js, ubah pembuatan token
    const token = jwt.sign(
      { 
        id: user.id, 
        username: user.username,
        roles: user.roles  // Tambahkan ini
      },
      process.env.JWT_SECRET,
      { expiresIn: '1h' }
    );

    // Di auth.js, endpoint login
    res.json({
      token,
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        roles: user.roles // Pastikan ini dikirimkan
      }
    });
  } catch (err) {
    console.error('Login error details:', {
      message: err.message,
      stack: err.stack,
      code: err.code
    });
    res.status(500).json({ 
      message: 'Terjadi kesalahan server',
      detail: process.env.NODE_ENV === 'development' ? err.message : undefined
    });
  }
});

// Di auth.js atau file yang menangani endpoint users
router.get('/users', async (req, res) => {
  try {
    const [users] = await pool.execute('SELECT * FROM users');
    console.log('Users from database:', users); // Tambahkan logging
    
    // Pastikan mengembalikan array
    res.json(users);
  } catch (err) {
    console.error('Error fetching users:', err);
    res.status(500).json({ message: 'Terjadi kesalahan server' });
  }
});

// Updated Password reset request endpoint
router.post('/reset-password', async (req, res) => {
  const { email } = req.body;

  try {
    // Check if user exists
    const [users] = await pool.execute(
      'SELECT * FROM users WHERE email = ?',
      [email]
    );

    if (users.length === 0) {
      return res.status(404).json({ message: 'Email tidak ditemukan' });
    }

    // Generate reset token
    const resetToken = crypto.randomBytes(32).toString('hex');
    const resetTokenHash = await bcrypt.hash(resetToken, 10);
    const tokenExpiry = new Date(Date.now() + 3600000); // 1 hour

    // Save token to database
    await pool.execute(
      'UPDATE users SET reset_token = ?, reset_token_expires = ? WHERE email = ?',
      [resetTokenHash, tokenExpiry, email]
    );

    // Send email using SendGrid
    try {
      await sendResetEmail(email, resetToken);
      res.json({ message: 'Link reset password telah dikirim ke email Anda' });
    } catch (emailError) {
      console.error('Failed to send reset email:', emailError);
      res.status(500).json({ 
        message: 'Gagal mengirim email reset password',
        detail: process.env.NODE_ENV === 'development' ? emailError.message : undefined
      });
    }

  } catch (err) {
    console.error('Reset password error:', err);
    res.status(500).json({ message: 'Terjadi kesalahan server' });
  }
});

router.post('/reset-password-confirm', async (req, res) => {
  const { newPassword } = req.body;

  try {
    // Check if token exists and not expired
    const [users] = await pool.execute(
      'SELECT * FROM users WHERE reset_token IS NOT NULL AND reset_token_expires > NOW()',
      []
    );

    if (users.length === 0) {
      return res.status(400).json({ 
        message: 'Token reset password tidak valid atau sudah kadaluarsa' 
      });
    }

    const user = users[0];

    // Hash new password
    const hashedPassword = await bcrypt.hash(newPassword, 10);

    // Update password and clear reset token
    await pool.execute(
      'UPDATE users SET password = ?, reset_token = NULL, reset_token_expires = NULL WHERE id = ?',
      [hashedPassword, user.id]
    );

    res.json({ message: 'Password berhasil direset' });
  } catch (err) {
    console.error('Reset password confirmation error:', err);
    res.status(500).json({ message: 'Terjadi kesalahan server' });
  }
});

router.post('/save-document', async (req, res) => {
  try {
    const { customTables, budgetSections } = req.body;
    
    // Validasi input dasar
    if (!customTables) {
      return res.status(400).json({ 
        error: 'Missing required data: customTables' 
      });
    }

    let result;
    
    // Cek apakah ini monthly table data
    if (customTables[0]?.headers?.[0]?.name === 'month') {
      // Validasi monthly table data
      if (!customTables[0]?.title || !customTables[0]?.sqlSafeName) {
        return res.status(400).json({
          error: 'Missing required monthly table data: title or sqlSafeName'
        });
      }
      result = await saveMonthlyTable(req.body);
    } else {
      // Validasi regular table data
      if (!budgetSections) {
        return res.status(400).json({ 
          error: 'Missing required data: budgetSections' 
        });
      }
      result = await saveToDatabase(customTables, budgetSections);
    }
    
    // Kirim response sukses dengan data yang tersimpan
    res.json({ 
      success: true, 
      data: result 
    });

  } catch (error) {
    console.error('Error saving to database:', error);
    res.status(500).json({ 
      error: error.message || 'Failed to save document' 
    });
  }
});

// Get all tables except 'users'
router.get('/tables', async (req, res) => {
  try {
    const [dbResult] = await pool.execute('SELECT DATABASE() as db');
    console.log('Current database:', dbResult[0].db);

    const [tables] = await pool.execute(`
      SELECT table_name 
      FROM information_schema.tables 
      WHERE table_schema = DATABASE()
      AND table_name != 'users'
    `);
    
    console.log('Raw tables result:', tables); // Tambahkan ini
    
    const tableNames = tables.map(table => table.TABLE_NAME);
    console.log('Formatted table names:', tableNames); // Tambahkan ini
    
    res.json(tableNames);
  } catch (err) {
    console.error('Error fetching tables:', err);
    res.status(500).json({ message: 'Terjadi kesalahan server' });
  }
});

// Get data from specific table
router.get('/tableData/:tableName', async (req, res) => {
  try {
    const tableName = req.params.tableName;
    const [rows] = await pool.execute(`SELECT * FROM ${tableName}`);
    res.json(rows);
  } catch (err) {
    console.error('Error fetching table data:', err);
    res.status(500).json({ message: 'Terjadi kesalahan server' });
  }
});

// Update cell value
router.post('/updateCell', async (req, res) => {
  try {
    const { table, id, column, value } = req.body;
    await pool.execute(
      `UPDATE ${table} SET ${column} = ? WHERE id = ?`,
      [value, id]
    );
    res.json({ message: 'Data berhasil diupdate' });
  } catch (err) {
    console.error('Error updating cell:', err);
    res.status(500).json({ message: 'Terjadi kesalahan server' });
  }
});

// Delete row
router.delete('/deleteRow', async (req, res) => {
  try {
    const { table, id } = req.body;
    await pool.execute(
      `DELETE FROM ${table} WHERE id = ?`,
      [id]
    );
    res.json({ message: 'Data berhasil dihapus' });
  } catch (err) {
    console.error('Error deleting row:', err);
    res.status(500).json({ message: 'Terjadi kesalahan server' });
  }
});

// Drop table
router.delete('/dropTable/:tableName', async (req, res) => {
  try {
    const tableName = req.params.tableName;
    await pool.execute(`DROP TABLE ${tableName}`);
    res.json({ message: 'Tabel berhasil dihapus' });
  } catch (err) {
    console.error('Error dropping table:', err);
    res.status(500).json({ message: 'Terjadi kesalahan server' });
  }
});

module.exports = router;