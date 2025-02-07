import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { Mail, AlertCircle } from 'lucide-react';

const ResetPassword = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [status, setStatus] = useState(''); // 'success' or 'error'
  const [isLoading, setIsLoading] = useState(false);

  const handleResetRequest = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');
    setStatus('');

    try {
      const apiUrl = 'http://localhost:5000/api/reset-password';  // Sesuaikan dengan URL backend Anda
      console.log('Sending reset password request to:', apiUrl);

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
        credentials: 'include', // Penting jika menggunakan cookies
      });

      const data = await response.json();
      console.log('Reset password response:', data);

      if (response.ok) {
        setStatus('success');
        setMessage('Link reset password telah dikirim ke email Anda');
      } else {
        setStatus('error');
        setMessage(data.message || 'Email tidak ditemukan dalam sistem');
      }
    } catch (err) {
      console.error('Reset password error:', err);
      setStatus('error');
      setMessage('Terjadi kesalahan pada server. Detail: ' + err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 flex items-center justify-center p-4">
      <Card className="w-full max-w-md bg-white/80 backdrop-blur-md shadow-xl">
        <CardHeader className="space-y-1 text-center">
          <CardTitle className="text-2xl font-bold">Reset Password</CardTitle>
          <p className="text-sm text-gray-600">
            Masukkan email Anda untuk menerima link reset password
          </p>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleResetRequest} className="space-y-4">
            {message && (
              <div className={`p-4 rounded-lg flex items-center gap-2 ${
                status === 'success' ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-600'
              }`}>
                <AlertCircle className="h-5 w-5" />
                {message}
              </div>
            )}
            <div className="relative">
              <Mail className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
              <Input
                type="email"
                placeholder="Email"
                className="pl-10"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={isLoading}
              />
            </div>
            <Button 
              type="submit" 
              className="w-full bg-blue-600 hover:bg-blue-700"
              disabled={isLoading}
            >
              {isLoading ? 'Mengirim...' : 'Kirim Link Reset Password'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default ResetPassword;