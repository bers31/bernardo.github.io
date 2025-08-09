# 🎓 Student Academic Information System (SIA-Univ)
*Comprehensive web-based academic management platform for universities*

<div align="center">

<img src="https://img.shields.io/badge/build-passing-brightgreen" alt="Build Status">
<img src="https://img.shields.io/badge/Laravel-10.x-red" alt="Laravel">
<img src="https://img.shields.io/badge/PHP-%3E%3D8.1-blue" alt="PHP Version">
<img src="https://img.shields.io/badge/MySQL-8.0-orange" alt="MySQL">
<img src="https://img.shields.io/badge/license-MIT-green" alt="License">

<p><strong><a href="https://bers31.github.io/bernardo.github.io/">🌐 Live Demo</a> | <a href="https://github.com/bers31/bernardo.github.io/tree/main">📁 Repository</a></strong></p>

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

<table width="100%" cellpadding="10" cellspacing="0" border="0">
<tr>
<td width="50%" valign="top">

<h3>👥 <strong>Multi-Role Dashboard</strong></h3>
<ul>
<li><strong>Student Portal</strong>: IRS management, KHS viewing, schedule tracking</li>
<li><strong>Lecturer Interface</strong>: Grade input, academic advising, teaching schedule</li>
<li><strong>Department Head</strong>: Course & schedule management</li>
<li><strong>Dean Panel</strong>: Approval workflows for room/schedule changes</li>
<li><strong>Admin Control</strong>: User management, data import/export</li>
</ul>

</td>
<td width="50%" valign="top">

<h3>🔐 <strong>Security & Authorization</strong></h3>
<ul>
<li>Laravel Authentication with role-based middleware</li>
<li>Encrypted password storage</li>
<li>Route protection per user role</li>
<li>Session management with logout functionality</li>
<li>Input validation and CSRF protection</li>
</ul>

</td>
</tr>
<tr>
<td width="50%" valign="top">

<h3>📊 <strong>Academic Management</strong></h3>
<ul>
<li><strong>IRS (Course Registration)</strong>: Student course selection with approval workflow</li>
<li><strong>KHS (Academic Transcript)</strong>: Semester grade reports</li>
<li><strong>Schedule Management</strong>: Room, time, and lecturer assignment</li>
<li><strong>Registration History</strong>: Payment and enrollment tracking</li>
<li><strong>Course Catalog</strong>: Complete curriculum management</li>
</ul>

</td>
<td width="50%" valign="top">

<h3>🚀 <strong>Modern Tech Stack</strong></h3>
<ul>
<li><strong>Backend</strong>: Laravel 10.x with Blade templating</li>
<li><strong>Database</strong>: MySQL with comprehensive relational design</li>
<li><strong>Frontend</strong>: Responsive UI with DataTables, SweetAlert2</li>
<li><strong>API</strong>: RESTful endpoints for dynamic data fetching</li>
<li><strong>Architecture</strong>: MVC pattern with resource controllers</li>
</ul>

</td>
</tr>
</table>

---

## 🛠️ **Technology Stack**

<div align="center">

<table width="100%" border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
<thead>
<tr style="background-color: #f6f8fa;">
<th><strong>Category</strong></th>
<th><strong>Technology</strong></th>
<th><strong>Version</strong></th>
<th><strong>Purpose</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Backend Framework</strong></td>
<td><img src="https://img.shields.io/badge/Laravel-FF2D20?style=flat&logo=laravel&logoColor=white" alt="Laravel"></td>
<td>10.x</td>
<td>Core framework</td>
</tr>
<tr>
<td><strong>Programming Language</strong></td>
<td><img src="https://img.shields.io/badge/PHP-777BB4?style=flat&logo=php&logoColor=white" alt="PHP"></td>
<td>≥8.1</td>
<td>Server-side logic</td>
</tr>
<tr>
<td><strong>Database</strong></td>
<td><img src="https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white" alt="MySQL"></td>
<td>8.0</td>
<td>Data persistence</td>
</tr>
<tr>
<td><strong>Template Engine</strong></td>
<td><img src="https://img.shields.io/badge/Blade-FF2D20?style=flat&logo=laravel&logoColor=white" alt="Blade"></td>
<td>Built-in</td>
<td>View rendering</td>
</tr>
<tr>
<td><strong>JavaScript Library</strong></td>
<td><img src="https://img.shields.io/badge/DataTables-1F4E79?style=flat" alt="DataTables"></td>
<td>Latest</td>
<td>Dynamic tables</td>
</tr>
<tr>
<td><strong>UI Components</strong></td>
<td><img src="https://img.shields.io/badge/SweetAlert2-7066E0?style=flat" alt="SweetAlert2"></td>
<td>Latest</td>
<td>Interactive alerts</td>
</tr>
<tr>
<td><strong>Package Manager</strong></td>
<td><img src="https://img.shields.io/badge/Composer-885630?style=flat&logo=composer&logoColor=white" alt="Composer"></td>
<td>Latest</td>
<td>Dependency management</td>
</tr>
</tbody>
</table>

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

<h3>🏠 <strong>Dashboard Overview</strong></h3>
<img src="https://bers31.github.io/bernardo.github.io/Student_Academic_Information_System/images/Picture11.png" alt="Student Dashboard" width="100%" style="max-width: 800px;">

<h3>📋 <strong>IRS Management System</strong></h3>
<img src="https://bers31.github.io/bernardo.github.io/Student_Academic_Information_System/images/Picture9.png" alt="IRS System" width="100%" style="max-width: 800px;">

<h3>📊 <strong>Admin Dashboard</strong></h3>
<img src="https://bers31.github.io/bernardo.github.io/Student_Academic_Information_System/images/Picture2.png" alt="Admin Dashboard" width="100%" style="max-width: 800px;">

<p><strong><a href="https://bers31.github.io/bernardo.github.io/">🔗 View Live Demo</a></strong></p>

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

<table width="100%" border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
<thead>
<tr style="background-color: #f6f8fa;">
<th><strong>Milestone</strong></th>
<th><strong>Features</strong></th>
<th><strong>Target Date</strong></th>
<th><strong>Status</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Phase 1</strong></td>
<td>Authentication & Basic CRUD</td>
<td>Q1 2024</td>
<td>✅ <strong>Completed</strong></td>
</tr>
<tr>
<td><strong>Phase 2</strong></td>
<td>IRS Management System</td>
<td>Q2 2024</td>
<td>✅ <strong>Completed</strong></td>
</tr>
<tr>
<td><strong>Phase 3</strong></td>
<td>Multi-Role Dashboards</td>
<td>Q2 2024</td>
<td>✅ <strong>Completed</strong></td>
</tr>
<tr>
<td><strong>Phase 4</strong></td>
<td>Advanced Reporting</td>
<td>Q3 2025</td>
<td>🔄 <strong>In Progress</strong></td>
</tr>
<tr>
<td><strong>Phase 5</strong></td>
<td>Mobile Optimization</td>
<td>Q4 2026</td>
<td>⏳ <strong>Planned</strong></td>
</tr>
<tr>
<td><strong>Phase 6</strong></td>
<td>API Integration & Export</td>
<td>Q1 2026</td>
<td>⏳ <strong>Planned</strong></td>
</tr>
</tbody>
</table>

</div>

---

## 🧪 **Testing & Development**

### **Quick Testing Checklist**
- [x] Authentication flow (login/logout)
- [x] Role-based dashboard access  
- [x] IRS creation and approval workflow
- [x] Schedule management (CRUD operations)
- [x] Grade input and KHS generation
- [x] Room change approval process
- [x] API endpoint responses
- [x] Database constraint validation

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
MIT License

Copyright (c) 2024 Bernardo - Universitas Diponegoro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 📫 Contact & Connect

<p align="center">
<strong>👨‍💻 Bernardo - Computer Science Student</strong><br/>
Universitas Diponegoro 🎓
</p>

<p align="center">
<a href="https://linkedin.com/in/bernardo-sunia/">
<img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
</a>
<a href="https://mail.google.com/mail/?view=cm&fs=1&to=suniabernardo@gmail.com">
<img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email">
</a>
<a href="https://github.com/bers31">
<img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
</a>
<a href="https://bit.ly/bernardo-my_portfolio">
<img src="https://img.shields.io/badge/Portfolio-255E63?style=for-the-badge&logo=About.me&logoColor=white" alt="Portfolio">
</a>
</p>

<p align="center">
⭐ <strong>If you found this project helpful, please give it a star!</strong> ⭐
</p>

<p align="center">
<em>Made with ❤️ by <a href="https://github.com/bers31">Bernardo</a> at Universitas Diponegoro</em><br/>
<img src="https://visitor-badge.laobi.icu/badge?page_id=bers31.bernardo.github.io" alt="Visitor Count">
</p>

---

### Full Screenshots
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
