import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent } from './ui/card';
import { 
  Building2, Users, Shield, Landmark, 
  Construction, Heart, UserPlus, LogOut, 
  ChevronRight 
} from 'lucide-react';

const DashboardPage = () => {
  const navigate = useNavigate();
  
  const sections = [
    {
      id: 'PEK',
      title: 'Perekonomian (PEK)',
      description: 'Kelola laporan keuangan untuk sektor perekonomian kecamatan',
      icon: Building2,
      color: 'bg-blue-500'
    },
    {
      id: 'UMPEG',
      title: 'Umum dan Kepegawaian (UMPEG)',
      description: 'Manajemen laporan keuangan untuk bagian kepegawaian',
      icon: Users,
      color: 'bg-green-500'
    },
    {
      id: 'TRANTIB',
      title: 'Ketentraman dan Ketertiban (TRANTIB)',
      description: 'Laporan keuangan untuk keamanan dan ketertiban',
      icon: Shield,
      color: 'bg-red-500'
    },
    {
      id: 'PEMERINTAHAN',
      title: 'Pemerintahan',
      description: 'Pengelolaan laporan keuangan administrasi pemerintahan',
      icon: Landmark,
      color: 'bg-purple-500'
    },
    {
      id: 'PEMBANGUNAN',
      title: 'Pembangunan',
      description: 'Manajemen keuangan untuk proyek pembangunan',
      icon: Construction,
      color: 'bg-orange-500'
    },
    {
      id: 'KESOS',
      title: 'Kesejahteraan Sosial (KESOS)',
      description: 'Laporan keuangan program kesejahteraan sosial',
      icon: Heart,
      color: 'bg-pink-500'
    },
    {
      id: 'PP',
      title: 'Pemberdayaan Perempuan (PP)',
      description: 'Pengelolaan laporan keuangan program pemberdayaan perempuan',
      icon: UserPlus,
      color: 'bg-teal-500'
    }
  ];

  const handleSectionClick = (sectionId) => {
    navigate(`/upload/${sectionId}`);
  };

  const handleLogout = () => {
    navigate('/');
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-200">
      <header className="bg-gradient-to-r from-indigo-400 via-blue-300 to-cyan-400 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex-1 flex justify-center items-center">
            <h1 className="text-2xl font-bold">Dashboard Keuangan</h1>
          </div>
          <button 
            className="flex justify-end text-black-600 hover:text-gray-900"
            onClick={handleLogout}
          >
            <LogOut className="h-5 w-5 mr-2" />
            Logout
          </button>
        </div>
      </header>

      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sections.map((section) => (
            <Card 
              key={section.id}
              className="hover:shadow-lg transition-shadow duration-200 cursor-pointer group"
              onClick={() => handleSectionClick(section.id)}
            >
              <CardContent className="p-6">
                <div className="flex items-start space-x-4">
                  <div className={`${section.color} p-3 rounded-lg`}>
                    <section.icon className="h-6 w-6 text-white" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg text-gray-900">
                      {section.title}
                    </h3>
                    <p className="text-sm text-gray-600 mt-1">
                      {section.description}
                    </p>
                  </div>
                  <ChevronRight className="h-5 w-5 text-gray-400 group-hover:text-gray-600 transition-colors duration-200" />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </main>
      <footer className="bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center">
          <p className="text-sm">
            &copy; {new Date().getFullYear()} Dashboard Keuangan. Dibuat dengan ❤️ oleh Bernardo. All Rights Reserved.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default DashboardPage;