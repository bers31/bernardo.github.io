const sgMail = require('@sendgrid/mail');

// Inisialisasi SendGrid dengan API key
sgMail.setApiKey(process.env.SENDGRID_API_KEY);

const sendResetEmail = async (userEmail, resetToken) => {
  try {
    console.log('SendGrid Configuration:', {
      apiKeyExists: !!process.env.SENDGRID_API_KEY,
      fromEmail: process.env.SMTP_FROM,
      toEmail: userEmail
    });
    
    let resetUrl;
    
    // Deteksi environment
    const isPackaged = process.env.NODE_ENV === 'production';
    
    if (isPackaged) {
      // Gunakan protokol kustom untuk deep linking
      resetUrl = `app://./reset-password/${resetToken}`;
    } else {
      // URL development
      resetUrl = `http://localhost:3000/#/reset-password/${resetToken}`;
    }
    
    const msg = {
      to: userEmail,
      from: {
        email: process.env.SENDGRID_FROM_EMAIL, // Email terverifikasi yang digunakan untuk autentikasi
        name: process.env.SMTP_FROM // Alamat fiktif yang akan terlihat sebagai pengirim
      },
      headers: {
        Sender: 'noreply@pemerintah.com' // Alamat fiktif yang terlihat
      },
      replyTo: 'noreply@pemerintah.com', // Memastikan penerima tidak dapat membalas
      subject: 'Reset Password - Sistem Manajemen Laporan Keuangan',
      html: `
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
          <h2 style="color: #1a365d;">Reset Password</h2>
          <p>Anda menerima email ini karena ada permintaan reset password untuk akun Anda.</p>
          <p>Silakan klik tombol di bawah ini untuk melanjutkan proses reset password:</p>
          <div style="text-align: center; margin: 30px 0;">
            <a href="${resetUrl}" 
               style="background-color: #2563eb; color: white; padding: 12px 24px; 
                      text-decoration: none; border-radius: 5px; display: inline-block;">
              Reset Password
            </a>
          </div>
          <p style="color: #64748b; font-size: 14px;">
            Link ini akan kadaluarsa dalam 1 jam.<br>
            Jika Anda tidak meminta reset password, abaikan email ini.
          </p>
          <div style="margin-top: 20px; text-align: center;">
            <p style="color: #64748b; font-size: 14px;">
              Jika tombol di atas tidak berfungsi, copy dan paste link berikut di browser Anda:
            </p>
            <p style="word-break: break-all; background-color: #f1f5f9; padding: 10px; 
                      border-radius: 4px; font-family: monospace; font-size: 12px;">
              ${resetUrl}
            </p>
          </div>
          <hr style="border: 1px solid #e2e8f0; margin: 20px 0;">
          <p style="color: #94a3b8; font-size: 12px; text-align: center;">
            Email ini dikirim secara otomatis, mohon tidak membalas email ini.
          </p>
        </div>
        </div>
      `
    };

    console.log('Attempting to send email with configuration:', {
      to: msg.to,
      from: process.env.SMTP_FROM,
      subject: msg.subject
    });

    const result = await sgMail.send(msg);
    console.log('Email sent successfully. Response:', result);
    
    return true;
  } catch (error) {
    // Log detailed error information
    console.error('SendGrid error details:', {
      message: error.message,
      code: error.code,
      response: error.response?.body,
      errors: error.response?.body?.errors
    });

    // Throw more specific error based on the response
    if (error.code === 403) {
      throw new Error('Authentication error: Periksa API key dan verifikasi email pengirim');
    } else if (error.response?.body?.errors) {
      throw new Error(`SendGrid error: ${error.response.body.errors[0].message}`);
    } else {
      throw new Error('Gagal mengirim email reset password: ' + error.message);
    }
  }
};

module.exports = { sendResetEmail };