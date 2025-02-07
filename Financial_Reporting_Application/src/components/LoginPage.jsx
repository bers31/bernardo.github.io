/* LoginPage.jsx */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { useAuth } from '../contexts/AuthContext';
import { 
  Lock,
  User,
  AlertCircle
} from 'lucide-react';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLocked, setIsLocked] = useState(false);
  const [lockTimer, setLockTimer] = useState(0);
  const navigate = useNavigate();
  const { login } = useAuth();

  useEffect(() => {
    let interval;
    if (lockTimer > 0) {
      interval = setInterval(() => {
        setLockTimer(prev => prev - 1);
      }, 1000);
    } else if (lockTimer === 0) {
      setIsLocked(false);
    }
    return () => clearInterval(interval);
  }, [lockTimer]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(''); // Clear previous errors
    
    if (isLocked) {
      setError(`Akun terkunci. Silakan tunggu ${lockTimer} detik`);
      return;
    }

    try {
      console.log('Attempting login...');
      
      const apiUrl = 'http://localhost:5000/api/login';  // Update URL to include full path
      console.log('Calling API:', apiUrl);
  
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
        credentials: 'include',
      });

      console.log('Response status:', response.status); // Debug log

      const data = await response.json();
      console.log('Response data:', data); // Debug log

      // Di LoginPage.jsx, tambahkan logging detail
      if (response.ok) {
        console.log('Full user data:', data.user); // Tambahkan ini
        login(data.token, data.user);
        if (data.user.roles === 'admin') {
          console.log('User is admin, redirecting to /admin'); // Tambahkan ini
          navigate('/admin');
        } else {
          console.log('User is not admin, redirecting to /dashboard'); // Tambahkan ini
          navigate('/dashboard');
        }
      } else {
        if (data.attemptsLeft === 5) {
          setIsLocked(true);
          setLockTimer(60);
          setError('Terlalu banyak percobaan gagal. Akun terkunci selama 1 menit');
        } else if (data.attemptsLeft === 0) {
          setError('Akun Anda telah diblokir. Silakan reset password Anda');
          navigate('/reset-password');
        } else {
          setError(`${data.message || 'Login gagal'}. ${data.attemptsLeft ? `Sisa percobaan: ${data.attemptsLeft}` : ''}`);
        }
      }
    } catch (err) {
      console.error('Login error:', err);
      setError('Terjadi kesalahan pada server. Silakan coba lagi nanti. Detail: ' + err.message);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-white/10 backdrop-blur-sm" />

      <Card className="w-full max-w-md bg-white/80 backdrop-blur-md shadow-xl">
        <CardHeader className="space-y-1 text-center">
          <CardTitle className="text-2xl font-bold tracking-tight">
            Sistem Manajemen Laporan Keuangan
          </CardTitle>
          <p className="text-sm text-gray-600">
            Kecamatan Semarang Timur
          </p>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleLogin} className="space-y-4">
            {error && (
              <div className="bg-red-50 p-4 rounded-lg flex items-center gap-2 text-red-600 text-sm">
                <AlertCircle className="h-5 w-5" />
                {error}
              </div>
            )}
            <div className="space-y-2">
              <div className="relative">
                <User className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
                <Input
                  type="text"
                  placeholder="Username"
                  className="pl-10"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  disabled={isLocked}
                />
              </div>
            </div>
            <div className="space-y-2">
              <div className="relative">
                <Lock className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
                <Input
                  type="password"
                  placeholder="Password"
                  className="pl-10"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={isLocked}
                />
              </div>
            </div>
            <div className="flex justify-between items-center text-sm">
              <Button
                type="button"
                variant="link"
                className="text-blue-600"
                onClick={() => navigate('/reset-password')}
              >
                Lupa Password?
              </Button>
            </div>
            <Button 
              type="submit" 
              className="w-full bg-blue-600 hover:bg-blue-700"
              disabled={isLocked}
            >
              {isLocked ? `Tunggu ${lockTimer} detik` : 'Login'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default Login;