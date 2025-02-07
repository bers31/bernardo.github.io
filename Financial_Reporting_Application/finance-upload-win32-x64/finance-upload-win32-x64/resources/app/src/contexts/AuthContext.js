import { createContext, useContext, useState, useEffect } from 'react';

// Membuat konteks autentikasi
const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [userRole, setUserRole] = useState(null);

  // Fungsi untuk mendekode JWT
  const decodeJWT = (token) => {
    try {
      const payload = token.split('.')[1]; // Ambil bagian payload
      return JSON.parse(atob(payload)); // Decode Base64 dan parse ke JSON
    } catch (error) {
      console.error('Invalid token:', error);
      return null;
    }
  };

  // Hook untuk memuat data autentikasi dari localStorage
  useEffect(() => {
    try {
      const storedAuth = localStorage.getItem('isAuthenticated');
      const storedUser = localStorage.getItem('user');
      const token = localStorage.getItem('token');

      if (storedAuth === 'true' && token) {
        const userData = decodeJWT(token); // Dekode token JWT
        if (userData) {
          setIsAuthenticated(true);
          setUser(JSON.parse(storedUser));
          setUserRole(userData.roles || 'guest');
        }
      }
    } catch (error) {
      console.error('Error loading authentication data:', error);
    }
  }, []);

  // Di AuthContext.jsx, fungsi login
  const login = (token, userData) => {
    try {
      const decodedData = decodeJWT(token);
      if (!decodedData) throw new Error('Invalid token.');
      
      console.log('Decoded token data:', decodedData);
      console.log('User data received:', userData);

      setIsAuthenticated(true);
      setUser(userData);
      setUserRole(userData.roles);  // Ubah dari role menjadi roles

      localStorage.setItem('isAuthenticated', 'true');
      localStorage.setItem('user', JSON.stringify(userData));
      localStorage.setItem('userRole', userData.roles);  // Ubah dari role menjadi roles
      localStorage.setItem('token', token);
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  // Fungsi logout
  const logout = async () => {
    try {
      await fetch('http://localhost:5000/api/logout', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });
    } catch (error) {
      console.error('Logout error:', error);
    }

    // Bersihkan state dan localStorage
    setIsAuthenticated(false);
    setUser(null);
    setUserRole(null);
    localStorage.clear();
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        user,
        userRole,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook untuk menggunakan AuthContext
export const useAuth = () => {
  return useContext(AuthContext);
};