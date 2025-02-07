// resetPasswordController.js
const express = require('express');
const { sendResetEmail } = require('./emailConfig');
const crypto = require('crypto');

const router = express.Router();

router.post('/api/reset-password', async (req, res) => {
  try {
    const { email } = req.body;

    // 1. Validasi email
    if (!email) {
      return res.status(400).json({ message: 'Email harus diisi' });
    }

    // 2. Cek apakah email ada di database
    const user = await User.findOne({ where: { email } });
    if (!user) {
      return res.status(404).json({ message: 'Email tidak ditemukan' });
    }

    // 3. Generate reset token
    const resetToken = crypto.randomBytes(32).toString('hex');
    const tokenExpiry = new Date(Date.now() + 3600000); // 1 jam

    // 4. Simpan token ke database
    await user.update({
      resetPasswordToken: resetToken,
      resetPasswordExpires: tokenExpiry
    });

    // 5. Kirim email
    try {
      await sendResetEmail(email, resetToken);
      res.json({ 
        success: true,
        message: 'Link reset password telah dikirim ke email Anda' 
      });
    } catch (emailError) {
      console.error('Email sending failed:', emailError);
      res.status(500).json({ 
        success: false,
        message: 'Gagal mengirim email reset password',
        detail: process.env.NODE_ENV === 'development' ? emailError.message : undefined
      });
    }

  } catch (error) {
    console.error('Reset password error:', error);
    res.status(500).json({ 
      success: false,
      message: 'Terjadi kesalahan server' 
    });
  }
});

module.exports = router;