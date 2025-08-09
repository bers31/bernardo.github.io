# 🎓 Student Academic Information System (SIA-Univ)
*Comprehensive web-based academic management platform for universities*

<div align="center">

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Laravel](https://img.shields.io/badge/Laravel-10.x-red)
![PHP Version](https://img.shields.io/badge/PHP-%3E%3D8.1-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![License](https://img.shields.io/badge/license-MIT-green)

**[🌐 Live Demo](https://bers31.github.io/bernardo.github.io/) | [📁 Repository](https://github.com/bers31/bernardo.github.io/tree/main)**

</div>

---

## 📖 **Project Overview**

SIA-Univ is a robust, full-featured **Academic Information System** built with Laravel that streamlines university administration processes. Designed for **Universitas Diponegoro**, this system provides comprehensive management for student enrollment, course scheduling, academic records, and multi-role authorization.

**Why SIA-Univ?**
- ✅ **Complete Academic Workflow** - From student registration to transcript generation
- ✅ **Role-Based Access Control** - Secure access for students, lecturers, heads of departments, deans, and administrators
- ✅ **Real-time Data Management** - Live updates for schedules, grades, and approvals
- ✅ **Professional UI/UX** - Modern, responsive interface with DataTables and SweetAlert2

---

## ✨ **Key Features**

<table>
<tr>
<td width="50%">

### 👥 **Multi-Role Dashboard**
- **Student Portal**: IRS management, KHS viewing, schedule tracking
- **Lecturer Interface**: Grade input, academic advising, teaching schedule
- **Department Head**: Course & schedule management
- **Dean Panel**: Approval workflows for room/schedule changes
- **Admin Control**: User management, data import/export

</td>
<td width="50%">

### 🔐 **Security & Authorization**
- Laravel Authentication with role-based middleware
- Encrypted password storage
- Route protection per user role
- Session management with logout functionality
- Input validation and CSRF protection

</td>
</tr>
<tr>
<td width="50%">

### 📊 **Academic Management**
- **IRS (Course Registration)**: Student course selection with approval workflow
- **KHS (Academic Transcript)**: Semester grade reports
- **Schedule Management**: Room, time, and lecturer assignment
- **Registration History**: Payment and enrollment tracking
- **Course Catalog**: Complete curriculum management

</td>
<td width="50%">

### 🚀 **Modern Tech Stack**
- **Backend**: Laravel 10.x with Blade templating
- **Database**: MySQL with comprehensive relational design
- **Frontend**: Responsive UI with DataTables, SweetAlert2
- **API**: RESTful endpoints for dynamic data fetching
- **Architecture**: MVC pattern with resource controllers

</td>
</tr>
</table>

---

## 🛠️ **Technology Stack**

<div align="center">

| **Category** | **Technology** | **Version** | **Purpose** |
|--------------|----------------|-------------|-------------|
| **Backend Framework** | <img src="https://img.shields.io/badge/Laravel-FF2D20?style=flat&logo=laravel&logoColor=white" alt="Laravel"> | 10.x | Core framework |
| **Programming Language** | <img src="https://img.shields.io/badge/PHP-777BB4?style=flat&logo=php&logoColor=white" alt="PHP"> | ≥8.1 | Server-side logic |
| **Database** | <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white" alt="MySQL"> | 8.0 | Data persistence |
| **Template Engine** | <img src="https://img.shields.io/badge/Blade-FF2D20?style=flat&logo=laravel&logoColor=white" alt="Blade"> | Built-in | View rendering |
| **JavaScript Library** | <img src="https://img.shields.io/badge/DataTables-1F4E79?style=flat" alt="DataTables"> | Latest | Dynamic tables |
| **UI Components** | <img src="https://img.shields.io/badge/SweetAlert2-7066E0?style=flat" alt="SweetAlert2"> | Latest | Interactive alerts |
| **Package Manager** | <img src="https://img.shields.io/badge/Composer-885630?style=flat&logo=composer&logoColor=white" alt="Composer"> | Latest | Dependency management |

</div>

---

## 🚀 **Installation & Setup**

### **Prerequisites**
- PHP ≥ 8.1
- Composer
- MySQL 8.0+
- Node.js & NPM (for asset compilation)

### **Quick Start**

```bash
# 1. Clone the repository
git clone https://github.com/bers31/bernardo.github.io.git
cd bernardo.github.io

# 2. Install PHP dependencies
composer install

# 3. Configure environment
cp .env.example .env
# Edit .env file with your database credentials:
# DB_DATABASE=project_pbp_preuts
# DB_USERNAME=your_username
# DB_PASSWORD=your_password

# 4. Generate application key
php artisan key:generate

# 5. Import database dump
mysql -u your_username -p project_pbp_preuts < file.sql

# 6. Run migrations (if additional migrations exist)
php artisan migrate --seed

# 7. Start development server
php artisan serve
```

**🎯 Access the application at:** `http://localhost:8000`

### **Default Accounts (Seed Data)**

| **Role** | **Email** | **Default Access** |
|----------|-----------|-------------------|
| **Admin** | `admin@example.com` | Full system access |
| **Student** | Check `users` table | Student dashboard |
| **Lecturer** | Check `users` table | Lecturer dashboard |

*Note: Passwords are encrypted in the database. Use Laravel Tinker or reset via email for secure access.*

---

## 🎥 **Demo & Screenshots**

<div align="center">

### 🏠 **Dashboard Overview**
<img src="https://via.placeholder.com/800x400/FF2D20/FFFFFF?text=Student+Dashboard+Preview" alt="Student Dashboard" width="100%">

### 📋 **IRS Management System**
<img src="https://via.placeholder.com/800x400/4479A1/FFFFFF?text=IRS+Course+Registration" alt="IRS System" width="100%">

### 📊 **Data Management Interface**
<img src="https://via.placeholder.com/800x400/28A745/FFFFFF?text=Admin+Data+Management" alt="Admin Panel" width="100%">

**[🔗 View Live Demo](https://bers31.github.io/bernardo.github.io/)**

</div>

---

## 🗄️ **Database Architecture**

### **Core Tables & Relationships**

```sql
-- Key Database Structure
users (id, email, username, password, role)
  ├── mahasiswa (nim, nama, kd_departemen) [FK: users.email]
  ├── dosen (nidn, nama, kd_departemen) [FK: users.email]
  
mata_kuliah (kode_mk, nama_mk, sks, semester)
  ├── jadwal (id, kode_mk, hari, jam_mulai, ruang) [FK: mata_kuliah.kode_mk]
  
irs (id, nim_mahasiswa, semester, status)
  ├── detail_irs (id_irs, kode_mk, nilai) [FK: irs.id, mata_kuliah.kode_mk]
  
fakultas → departemen → prodi (hierarchical structure)
tahun_ajaran (id, tahun, semester, status_aktif)
```

### **Entity Relationship Highlights**
- **Users Authentication**: Central auth table with role-based access
- **Academic Hierarchy**: Faculty → Department → Study Program structure  
- **Course Management**: Course catalog with scheduling constraints
- **Student Records**: IRS enrollment with detailed grade tracking
- **Approval Workflow**: Multi-level approval system for academic changes

---

## 🔗 **API Endpoints & Routing**

### **Public Routes**
```php
GET  /               # Welcome page
GET  /about          # About page  
POST /login          # Authentication
POST /logout         # User logout
```

### **Role-Based Protected Routes**

<details>
<summary><b>👨‍🎓 Student Routes</b> <code>/mahasiswa/*</code></summary>

```php
GET  /mahasiswa/dashboard        # Student dashboard
GET  /mahasiswa/status_akademik  # Academic status
GET  /mahasiswa/registrasi_mhs   # Registration management
GET  /mahasiswa/irs_mhs          # IRS course selection
GET  /mahasiswa/jadwal_mhs       # Class schedule
GET  /mahasiswa/khs_mhs          # Semester grades
GET  /mahasiswa/transkrip_mhs    # Academic transcript
```
</details>

<details>
<summary><b>👨‍🏫 Lecturer Routes</b> <code>/dosen/*</code></summary>

```php
GET  /dosen/dashboard     # Lecturer dashboard
GET  /dosen/perwalian     # Academic advising
GET  /dosen/input_nilai   # Grade input interface
GET  /dosen/jadwal        # Teaching schedule
```
</details>

<details>
<summary><b>🏛️ Administrative Routes</b></summary>

```php
# Department Head
Resource /kaprodi/matkul    # Course management
Resource /kaprodi/jadwal    # Schedule management

# Dean Panel  
POST /dekan/approve-room-change/{id}  # Room change approval
POST /dekan/approveAllRoomChanges     # Bulk approval

# Admin Panel
Resource /admin/users       # User management
Resource /admin/mahasiswa   # Student data
Resource /admin/dosen       # Lecturer data
```
</details>

### **API Endpoints**
```bash
# Data Fetching APIs
GET  /api/jadwal              # Schedule data (JSON)
GET  /api/fetch-dosen         # Lecturer list
GET  /api/fetch-mahasiswa     # Student data
POST /api/approve-irs/{id}    # IRS approval

# Report Generation
GET  /mhs/print_irs/{nim}/{semester}  # IRS PDF export
```

---

## 📈 **Project Roadmap**

<div align="center">

| **Milestone** | **Features** | **Target Date** | **Status** |
|---------------|--------------|-----------------|------------|
| **Phase 1** | Authentication & Basic CRUD | Q1 2024 | ✅ **Completed** |
| **Phase 2** | IRS Management System | Q2 2024 | ✅ **Completed** |
| **Phase 3** | Multi-Role Dashboards | Q2 2024 | ✅ **Completed** |
| **Phase 4** | Advanced Reporting | Q3 2024 | 🔄 **In Progress** |
| **Phase 5** | Mobile Optimization | Q4 2024 | ⏳ **Planned** |
| **Phase 6** | API Integration & Export | Q1 2025 | ⏳ **Planned** |

</div>

---

## 🧪 **Testing & Development**

### **Quick Testing Checklist**
- [ ] Authentication flow (login/logout)
- [ ] Role-based dashboard access  
- [ ] IRS creation and approval workflow
- [ ] Schedule management (CRUD operations)
- [ ] Grade input and KHS generation
- [ ] Room change approval process
- [ ] API endpoint responses
- [ ] Database constraint validation

### **Development Guidelines**
```bash
# Adding new controller
php artisan make:controller NewController --resource

# Creating middleware
php artisan make:middleware CustomMiddleware  

# Database migrations
php artisan make:migration create_new_table

# Testing routes
php artisan route:list --name=mahasiswa
```

---

## 🤝 **Contributing**

We welcome contributions to improve SIA-Univ! Here's how you can help:

1. **🍴 Fork** the repository
2. **🔧 Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **💾 Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **📤 Push** to the branch (`git push origin feature/amazing-feature`)
5. **🔀 Open** a Pull Request

### **Development Standards**
- Follow PSR-12 coding standards
- Write descriptive commit messages
- Include tests for new features
- Update documentation as needed

---

## 📄 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
Copyright (c) 2024 Bernardo - Universitas Diponegoro
Permission is hereby granted, free of charge, to any person obtaining a copy...
```

---

## 📫 **Contact & Support**

<div align="center">

### 👨‍💻 **Developer Information**

**Bernardo**  
*Computer Science Student - Universitas Diponegoro*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/your-linkedin)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:your.email@example.com)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/bers31)

---

### 🌟 **Show Your Support**

If this project helped you, please ⭐ **star this repository** and share it with others!

**Built with ❤️ for the academic community**

</div>

---

<div align="center">
<sub>🎓 Empowering Education Through Technology | Made with Laravel & MySQL</sub>
</div>

### Screenshots
![Screenshot 1](images/Picture14.png)
![Screenshot 2](images/Picture.png)
![Screenshot 3](images/Picture1.png)
![Screenshot 4](images/Picture2.png)
![Screenshot 5](images/Picture3.png)
![Screenshot 6](images/Picture4.png)
![Screenshot 7](images/Picture5.png)
![Screenshot 8](images/Picture6.png)
![Screenshot 9](images/Picture7.png)
![Screenshot 10](images/Picture8.png)
![Screenshot 11](images/Picture9.png)
![Screenshot 12](images/Picture10.png)
![Screenshot 13](images/Picture13.png)
![Screenshot 14](images/Picture11.png)
![Screenshot 15](images/Picture12.png)
![Screenshot 16](images/Picture15.png)
![Screenshot 17](images/Picture16.png)
![Screenshot 18](images/Picture17.png)
![Screenshot 19](images/Picture18.png)

## Conclusion
This project demonstrates the development of an efficient academic information system using Laravel, MySQL, and JavaScript, providing a seamless experience for students and academic advisors.
