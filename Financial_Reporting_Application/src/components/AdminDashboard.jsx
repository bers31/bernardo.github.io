import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardFooter, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from './ui/dialog';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from './ui/table';
import {
  UserPlus,
  Edit2,
  Trash2,
  Search,
  RefreshCw,
  LogOut,
  AlertCircle
} from 'lucide-react';
import { Alert, AlertDescription } from './ui/alert';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedUser, setSelectedUser] = useState(null);
  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    roles: 'keuangan',
    password: '',
  });

  const roles = [
    'camat',
    'sekcam',
    'admin',
    'keuangan',
    'kepegawaian',
    'pemerintahan',
    'pembangunan',
    'perekonomian',
    'pelayanan',
    'tantrib'
  ];

  const roleColors = {
    camat: 'bg-purple-100 text-purple-800',
    sekcam: 'bg-blue-100 text-blue-800',
    admin: 'bg-red-100 text-red-800',
    keuangan: 'bg-green-100 text-green-800',
    kepegawaian: 'bg-yellow-100 text-yellow-800',
    pemerintahan: 'bg-indigo-100 text-indigo-800',
    pembangunan: 'bg-pink-100 text-pink-800',
    perekonomian: 'bg-orange-100 text-orange-800',
    pelayanan: 'bg-teal-100 text-teal-800',
    tantrib: 'bg-gray-100 text-gray-800'
  };

  const handleLogout = () => {
    navigate('/');
  };

  const fetchUsers = async () => {
    try {
      setIsLoading(true); // Tambahkan loading state
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No token found');
      }
  
      const response = await fetch('http://localhost:5000/api/users', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      
      if (Array.isArray(data)) {
        setUsers(data); // Pastikan state users terupdate
        console.log('Data fetched:', data); // Tambahkan log untuk debugging
      } else {
        throw new Error('Invalid data format received');
      }
  
      setError('');
    } catch (error) {
      console.error('Error fetching users:', error);
      setError(`Error fetching users: ${error.message}`);
      setUsers([]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleCreateUser = async () => {
    try {
      if (!formData.username || !formData.email || !formData.roles || !formData.password) {
        setError('Semua field harus diisi');
        return;
      }
      
      const response = await fetch('http://localhost:5000/api/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Failed to create user');
      }

      await fetchUsers();
      setIsAddDialogOpen(false);
      setFormData({ username: '', email: '', roles: 'keuangan', password: '' });
      setError('');
    } catch (error) {
      console.error('Error creating user:', error);
      setError('Error creating user: ' + error.message);
    }
  };

  const handleUpdateUser = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/users/${selectedUser.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Failed to update user');
      }

      await fetchUsers();
      setIsEditDialogOpen(false);
      setSelectedUser(null);
      setFormData({ username: '', email: '', roles: 'keuangan', password: '' });
      setError('');
    } catch (error) {
      console.error('Error updating user:', error);
      setError('Error updating user: ' + error.message);
    }
  };

  const handleDeleteUser = async (userId) => {
    if (window.confirm('Apakah Anda yakin ingin menghapus pengguna ini?')) {
      try {
        const response = await fetch(`http://localhost:5000/api/users/${userId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || 'Failed to delete user');
        }

        await fetchUsers();
        setError('');
      } catch (error) {
        console.error('Error deleting user:', error);
        setError('Error deleting user: ' + error.message);
      }
    }
  };

  const filteredUsers = Array.isArray(users) ? users.filter(user =>
    user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.roles.toLowerCase().includes(searchTerm.toLowerCase())
  ) : [];

  return (
    <div className="min-h-screen flex flex-col">
      <Card className="flex flex-col flex-grow max-w-7xl mx-auto">
        <CardHeader className="flex flex-row items-center justify-between space-x-4 p-4 bg-green-200 ">
          <div>
            <CardTitle className="text-2xl font-bold">User Management</CardTitle>
            <button 
              className="flex items-center text-black-600 hover:text-gray-900 py-3"
              onClick={handleLogout}
            >
              <LogOut className="h-5 w-5 mr-2" />
              Logout
            </button>
          </div>
          <div className="flex items-center gap-4">
          <Button
            onClick={async () => {
              setIsLoading(true);
              try {
                await fetchUsers();
                setError('');
              } catch (error) {
                setError('Error refreshing data: ' + error.message);
              } finally {
                setIsLoading(false);
              }
            }}
            variant="outline"
            size="icon"
            className="hover:bg-gray-100"
            disabled={isLoading}
          >
            <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
          </Button>

            {/* Tombol Add User */}
            <Button 
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 flex items-center gap-2"
              onClick={() => {
                setFormData({ username: '', email: '', roles: 'keuangan', password: '' });
                setError('');
                setIsAddDialogOpen(true);
              }}
            >
              <UserPlus className="h-5 w-5" />
              <span>Tambah User</span>
            </Button>
            
            {/* Add User Dialog */}
            <Dialog open={isAddDialogOpen} onOpenChange={setIsAddDialogOpen}>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Create New User</DialogTitle>
                </DialogHeader>
                <div className="space-y-4 py-4">
                  {error && (
                    <Alert variant="destructive">
                      <AlertCircle className="h-4 w-4" />
                      <AlertDescription>{error}</AlertDescription>
                    </Alert>
                  )}
                  <Input
                    placeholder="Username"
                    value={formData.username}
                    onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                    required
                  />
                  <Input
                    placeholder="Email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    required
                  />
                  <select
                    className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={formData.roles}
                    onChange={(e) => setFormData({ ...formData, roles: e.target.value })}
                    required
                  >
                    {roles.map((role) => (
                      <option key={role} value={role}>
                        {role.charAt(0).toUpperCase() + role.slice(1)}
                      </option>
                    ))}
                  </select>
                  <Input
                    placeholder="Password"
                    type="password"
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    required
                  />
                  <Button
                    className="w-full bg-gray-300"
                    onClick={handleCreateUser}
                  >
                    Create User
                  </Button>
                </div>
              </DialogContent>
            </Dialog>

            {/* Edit User Dialog */}
            <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Edit User</DialogTitle>
                </DialogHeader>
                <div className="space-y-4 py-4">
                  {error && (
                    <Alert variant="destructive">
                      <AlertCircle className="h-4 w-4" />
                      <AlertDescription>{error}</AlertDescription>
                    </Alert>
                  )}
                  <Input
                    placeholder="Username"
                    value={formData.username}
                    onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                    required
                  />
                  <Input
                    placeholder="Email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    required
                  />
                  <select
                    className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={formData.roles}
                    onChange={(e) => setFormData({ ...formData, roles: e.target.value })}
                    required
                  >
                    {roles.map((role) => (
                      <option key={role} value={role}>
                        {role.charAt(0).toUpperCase() + role.slice(1)}
                      </option>
                    ))}
                  </select>
                  <Button
                    className="w-full"
                    onClick={handleUpdateUser}
                  >
                    Update User
                  </Button>
                </div>
              </DialogContent>
            </Dialog>
          </div>
        </CardHeader>
        <CardContent className="flex-grow">
          {error && (
            <Alert variant="destructive" className="mb-4">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                {error}
              </AlertDescription>
            </Alert>
          )}
          {isLoading ? (
            <div className="flex justify-center items-center h-48">
              <RefreshCw className="h-8 w-8 animate-spin text-gray-400" />
            </div>
          ) : (
            <>
              <div className="relative mb-4 py-5">
                <Search className="absolute left-3 top-8 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Search users..."
                  className="pl-10"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
              <p className="text-sm text-gray-500">
                Total Users: {users.length}
              </p>
              <div className="border rounded-lg overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Username</TableHead>
                      <TableHead>Email</TableHead>
                      <TableHead>Role</TableHead>
                      <TableHead>Created At</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredUsers.map((user) => (
                      <TableRow key={user.id}>
                        <TableCell className="font-medium">{user.username}</TableCell>
                        <TableCell>{user.email}</TableCell>
                        <TableCell>
                          <span className={`px-2 py-1 rounded-full text-xs ${roleColors[user.roles] || 'bg-gray-100 text-gray-800'}`}>
                            {user.roles}
                          </span>
                        </TableCell>
                        <TableCell>
                          {new Date(user.created_at).toLocaleDateString()}
                        </TableCell>
                        <TableCell className="text-right">
                          <Button
                            variant="ghost"
                            size="icon"
                            className="hover:bg-gray-100"
                            onClick={() => {
                              setSelectedUser(user);
                              setFormData({
                                username: user.username,
                                email: user.email,
                                roles: user.roles,
                                password: '',
                              });
                              setError('');
                              setIsEditDialogOpen(true);
                            }}
                          >
                            <Edit2 className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="icon"
                            className="hover:bg-red-100"
                            onClick={() => handleDeleteUser(user.id)}
                          >
                            <Trash2 className="h-4 w-4 text-red-500" />
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </>
          )}
        </CardContent>
        <CardFooter className="w-full bg-gray-800 text-white mt-auto">
          <p className="max-w-7xl mx-auto py-4 px-8 text-center">
            &copy; {new Date().getFullYear()} Dashboard Admin. Dibuat dengan ❤️ oleh Bernardo. All Rights Reserved.
          </p>
        </CardFooter>
      </Card>
    </div>
  );
};

export default AdminDashboard;