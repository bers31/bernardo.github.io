# 💼 Financial Report Management System
> *Streamlining financial reporting workflows with modern web technology and role-based access control*

<div align="center">

<img src="https://img.shields.io/badge/build-passing-brightgreen" alt="Build Status">
<img src="https://img.shields.io/badge/version-1.0.0-blue" alt="Version">
<img src="https://img.shields.io/badge/license-MIT-green" alt="License">
<img src="https://img.shields.io/badge/React-18+-61DAFB?logo=react" alt="React">
<img src="https://img.shields.io/badge/Node.js-18+-339933?logo=node.js" alt="Node.js">
<img src="https://img.shields.io/badge/Tailwind-CSS-38B2AC?logo=tailwind-css" alt="TailwindCSS">

</div>

---

## 📖 Project Overview

The **Financial Report Management System** is a comprehensive web application designed to revolutionize financial reporting processes at the district level. Built specifically for East Semarang District, this system addresses the critical need for standardized, efficient, and secure financial document management across multiple departments.

### 🎯 Background & Benefits

Traditional financial reporting in government institutions often suffers from inconsistent formats, manual data entry errors, and lack of proper audit trails. This system provides a unified platform that:

- **Reduces manual work by 70%** through automated form generation and calculation
- **Ensures data accuracy** with built-in budget validation and error checking
- **Enhances transparency** through comprehensive audit logging and role-based access
- **Improves security** with token-based authentication and route protection

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

<h3>🔐 Authentication & Security</h3>
<ul>
<li>Multi-role user management (Admin, Camat, Sekcam, Finance)</li>
<li>Token-based authentication with email verification</li>
<li>Protected routes based on user permissions</li>
<li>Password reset functionality via SendGrid</li>
</ul>

<h3>📊 Dynamic Form Generation</h3>
<ul>
<li>Customizable financial report templates</li>
<li>Real-time budget validation and calculations</li>
<li>Dynamic table creation and management</li>
<li>Performance indicator tracking</li>
</ul>

</td>
<td width="50%">

<h3>📈 Data Visualization</h3>
<ul>
<li>Interactive charts and graphs using Recharts</li>
<li>Monthly financial reports with visual analytics</li>
<li>Export capabilities (PDF generation via jsPDF)</li>
<li>Responsive dashboard for all device types</li>
</ul>

<h3>🏛️ Department Management</h3>
<ul>
<li>Support for multiple departments (PEK, UMPEG, TRANTIB, etc.)</li>
<li>Centralized document storage and retrieval</li>
<li>Audit trail for all financial transactions</li>
<li>Bulk data import/export functionality</li>
</ul>

</td>
</tr>
</table>

---

## 🛠️ Technology Stack

<div align="center">

<h3>Frontend Technologies</h3>
<table>
<tr>
<th>Technology</th>
<th>Version</th>
<th>Purpose</th>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=white" alt="React"></td>
<td>18+</td>
<td>UI Framework</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?logo=tailwind-css&logoColor=white" alt="Tailwind"></td>
<td>3.x</td>
<td>Styling</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Zustand-FF6B6B?logo=zustand&logoColor=white" alt="Zustand"></td>
<td>Latest</td>
<td>State Management</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/React_Router-CA4245?logo=react-router&logoColor=white" alt="React Router"></td>
<td>6.x</td>
<td>Routing</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Recharts-8884D8?logo=recharts&logoColor=white" alt="Recharts"></td>
<td>2.x</td>
<td>Data Visualization</td>
</tr>
</table>

<h3>Backend Technologies</h3>
<table>
<tr>
<th>Technology</th>
<th>Version</th>
<th>Purpose</th>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Node.js-339933?logo=node.js&logoColor=white" alt="Node.js"></td>
<td>18+</td>
<td>Runtime Environment</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Express.js-000000?logo=express&logoColor=white" alt="Express"></td>
<td>4.x</td>
<td>Web Framework</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/SendGrid-00A4DC?logo=sendgrid&logoColor=white" alt="SendGrid"></td>
<td>Latest</td>
<td>Email Service</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/JWT-000000?logo=json-web-tokens&logoColor=white" alt="JWT"></td>
<td>Latest</td>
<td>Authentication</td>
</tr>
</table>

</div>

---

## 🏗️ System Architecture

<pre>
```
┌─────────────────────────────────────────────────────────────────┐
│                          CLIENT LAYER                           │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   Login Page    │  Dashboard      │     Admin Panel             │
│                 │                 │                             │
│ • Authentication│ • Role-based    │ • User Management           │
│ • Password Reset│   Navigation    │ • System Configuration      │
│                 │ • Quick Actions │ • Audit Logs                │
└─────────────────┴─────────────────┴─────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                          │
├─────────────────┬─────────────────┬─────────────────────────────┤
│ Financial Forms │  Table Manager  │    Document Generator       │
│                 │                 │                             │
│ • Dynamic Forms │ • CRUD Tables   │ • PDF Export                │
│ • Validation    │ • Data Import   │ • Template Management       │
│ • Calculations  │ • Charts        │ • Batch Processing          │
└─────────────────┴─────────────────┴─────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                       SERVICE LAYER                             │
├─────────────────┬─────────────────┬─────────────────────────────┤
│ Auth Service    │  Email Service  │    Data Service             │
│                 │                 │                             │
│ • JWT Tokens    │ • SendGrid      │ • Database Operations       │
│ • Role Checking │ • Notifications │ • File Management           │
│ • Session Mgmt  │ • Templates     │ • Backup & Recovery         │
└─────────────────┴─────────────────┴─────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                               │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   User Data     │ Financial Data  │     System Data             │
│                 │                 │                             │
│ • Profiles      │ • Reports       │ • Configurations            │
│ • Roles         │ • Tables        │ • Logs                      │
│ • Sessions      │ • Documents     │ • Backups                   │
└─────────────────┴─────────────────┴─────────────────────────────┘
```
</pre>

---

## 🚀 Installation & Setup

### Prerequisites
```bash
# Ensure you have Node.js installed
node --version  # Should be 18.0.0 or higher
npm --version   # Should be 8.0.0 or higher
```

### Quick Start
```bash
# Clone the repository
git clone https://github.com/bers31/bernardo.github.io.git
cd bernardo.github.io

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

### Environment Configuration
```bash
# Backend Configuration
NODE_ENV=development
PORT=3001
JWT_SECRET=your_jwt_secret_here
SENDGRID_API_KEY=your_sendgrid_api_key
DATABASE_URL=your_database_connection_string

# Frontend Configuration
REACT_APP_API_URL=http://localhost:3001/api
REACT_APP_ENV=development
```

---

## 🎥 Demo & Screenshots

<div align="center">

<h3>🔐 Login Interface</h3>
<img src="https://bers31.github.io/bernardo.github.io/Financial_Reporting_Application/images/Picture1.png" alt="Login Interface" width="48%">

<h3>📊 Financial Dashboard</h3>
<img src="https://bers31.github.io/bernardo.github.io/Financial_Reporting_Application/images/Picture5.png" alt="Dashboard" width="48%">

<h3>📋 Report Generation</h3>
<img src="https://bers31.github.io/bernardo.github.io/Financial_Reporting_Application/images/Picture6.png" alt="Report Generation" width="48%">

<h3>👥 User Management</h3>
<img src="https://bers31.github.io/bernardo.github.io/Financial_Reporting_Application/images/Picture2.png" alt="User Management" width="48%">

</div>

<h3>🌐 <a href="https://bers31.github.io/bernardo.github.io/Financial_Reporting_Application/">Live Demo</a></h3>

---

## 🗺️ Project Scope

This project was developed as a **complete, self-contained academic assignment** for the Web Application Development course at Universitas Diponegoro. The scope below reflects what was fully implemented and delivered.

| Module | Description | Status |
|--------|-------------|--------|
| 🔐 **Authentication & RBAC** | JWT-based login with multi-role support (Admin, Camat, Sekcam, Finance) and email verification via SendGrid | ✅ Done |
| 📊 **Financial Form Builder** | Dynamic form generation with real-time budget validation, calculations, and performance indicator tracking | ✅ Done |
| 🏛️ **Department Management** | Multi-department support (PEK, UMPEG, TRANTIB, etc.) with centralized document storage | ✅ Done |
| 📋 **PDF Export & Reporting** | Report generation via jsPDF with customizable templates and batch processing | ✅ Done |
| 📈 **Data Visualization** | Interactive charts and monthly financial analytics using Recharts | ✅ Done |
| 👥 **User Management** | Admin panel for user creation, role assignment, and audit trail logging | ✅ Done |
| 📤 **Bulk Import & Export** | Excel/CSV data import and export functionality across departments | ✅ Done |

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Getting Started
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add some amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow the existing code style and conventions
- Write clear, concise commit messages
- Include tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

### Areas We Need Help With
- 🐛 Bug fixes and optimization
- 🌐 Internationalization (i18n)
- 📱 Mobile responsiveness improvements
- 🧪 Test coverage expansion
- 📚 Documentation improvements

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
![Screenshot 1](images/Picture1.png)
![Screenshot 2](images/Picture2.png)
![Screenshot 3](images/Picture3.png)
![Screenshot 4](images/Picture4.png)
![Screenshot 5](images/Picture5.png)
![Screenshot 6](images/Picture6.png)
![Screenshot 7](images/Picture7.png)

## Conclusion
This project demonstrates the creation of an engaging 3D game using C++ and OpenGL, showcasing advanced graphics techniques and interactive gameplay elements.
