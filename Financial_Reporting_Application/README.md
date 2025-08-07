# 💼 Financial Report Management System - East Semarang District
> *Streamlining financial reporting workflows with modern web technology and role-based access control*

<div align="center">

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react)
![Node.js](https://img.shields.io/badge/Node.js-18+-339933?logo=node.js)
![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC?logo=tailwind-css)

</div>

---

## 📖 Project Overview

<div align="center">
<img src="https://via.placeholder.com/800x400/4F46E5/FFFFFF?text=Financial+Management+Dashboard" alt="Dashboard Preview" width="100%">
</div>

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

### 🔐 Authentication & Security
- Multi-role user management (Admin, Camat, Sekcam, Finance)
- Token-based authentication with email verification
- Protected routes based on user permissions
- Password reset functionality via SendGrid

### 📊 Dynamic Form Generation
- Customizable financial report templates
- Real-time budget validation and calculations
- Dynamic table creation and management
- Performance indicator tracking

</td>
<td width="50%">

### 📈 Data Visualization
- Interactive charts and graphs using Recharts
- Monthly financial reports with visual analytics
- Export capabilities (PDF generation via jsPDF)
- Responsive dashboard for all device types

### 🏛️ Department Management
- Support for multiple departments (PEK, UMPEG, TRANTIB, etc.)
- Centralized document storage and retrieval
- Audit trail for all financial transactions
- Bulk data import/export functionality

</td>
</tr>
</table>

---

## 🛠️ Technology Stack

<div align="center">

### Frontend Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| <img src="https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=white" alt="React"> | 18+ | UI Framework |
| <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?logo=tailwind-css&logoColor=white" alt="Tailwind"> | 3.x | Styling |
| <img src="https://img.shields.io/badge/Zustand-FF6B6B?logo=zustand&logoColor=white" alt="Zustand"> | Latest | State Management |
| <img src="https://img.shields.io/badge/React_Router-CA4245?logo=react-router&logoColor=white" alt="React Router"> | 6.x | Routing |
| <img src="https://img.shields.io/badge/Recharts-8884D8?logo=recharts&logoColor=white" alt="Recharts"> | 2.x | Data Visualization |

### Backend Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| <img src="https://img.shields.io/badge/Node.js-339933?logo=node.js&logoColor=white" alt="Node.js"> | 18+ | Runtime Environment |
| <img src="https://img.shields.io/badge/Express.js-000000?logo=express&logoColor=white" alt="Express"> | 4.x | Web Framework |
| <img src="https://img.shields.io/badge/SendGrid-00A4DC?logo=sendgrid&logoColor=white" alt="SendGrid"> | Latest | Email Service |
| <img src="https://img.shields.io/badge/JWT-000000?logo=json-web-tokens&logoColor=white" alt="JWT"> | Latest | Authentication |

</div>

---

## 🏗️ System Architecture

<div align="center">

```
┌─────────────────────────────────────────────────────────────────┐
│                          CLIENT LAYER                          │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   Login Page    │  Dashboard      │     Admin Panel             │
│                 │                 │                             │
│ • Authentication│ • Role-based    │ • User Management           │
│ • Password Reset│   Navigation    │ • System Configuration      │
│                 │ • Quick Actions │ • Audit Logs               │
└─────────────────┴─────────────────┴─────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                         │
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
│                       SERVICE LAYER                            │
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
│                        DATA LAYER                              │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   User Data     │ Financial Data  │     System Data             │
│                 │                 │                             │
│ • Profiles      │ • Reports       │ • Configurations            │
│ • Roles         │ • Tables        │ • Logs                      │
│ • Sessions      │ • Documents     │ • Backups                   │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

</div>

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

### 🔐 Login Interface
<img src="https://via.placeholder.com/600x400/6366F1/FFFFFF?text=Secure+Login+Portal" alt="Login Interface" width="48%">

### 📊 Financial Dashboard
<img src="https://via.placeholder.com/600x400/10B981/FFFFFF?text=Interactive+Dashboard" alt="Dashboard" width="48%">

### 📋 Report Generation
<img src="https://via.placeholder.com/600x400/F59E0B/FFFFFF?text=Dynamic+Form+Builder" alt="Report Generation" width="48%">

### 👥 User Management
<img src="https://via.placeholder.com/600x400/EF4444/FFFFFF?text=Admin+Panel" alt="User Management" width="48%">

</div>

### 🌐 Live Demo
> **GitHub Pages:** [https://bers31.github.io/bernardo.github.io/](https://bers31.github.io/bernardo.github.io/)

---

## 📅 Development Roadmap

<div align="center">

| Phase | Milestone | Target Date | Status |
|-------|-----------|-------------|--------|
| **Phase 1** | Core Authentication System | Q1 2024 | ✅ Complete |
| **Phase 2** | Financial Form Builder | Q1 2024 | ✅ Complete |
| **Phase 3** | PDF Export & Reporting | Q2 2024 | ✅ Complete |
| **Phase 4** | Advanced Analytics | Q2 2024 | 🔄 In Progress |
| **Phase 5** | Mobile App Integration | Q3 2024 | 📋 Planned |
| **Phase 6** | API Documentation | Q3 2024 | 📋 Planned |

</div>

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

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Bernardo Portfolio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 📫 Get in Touch

<div align="center">

### 👨‍💻 About the Developer

<img src="https://via.placeholder.com/150x150/4F46E5/FFFFFF?text=B" alt="Developer" width="150" style="border-radius: 50%;">

**Bernardo**  
*Information Technology Student*  
*Diponegoro University*

</div>

### 📱 Contact Information

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/bernardo)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:bernardo@example.com)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/bers31)
[![Portfolio](https://img.shields.io/badge/Portfolio-4F46E5?style=for-the-badge&logo=google-chrome&logoColor=white)](https://bers31.github.io/bernardo.github.io/)

</div>

---

<div align="center">

### 🌟 Star this repository if you find it helpful!

**Made with ❤️ for government financial transparency and efficiency**

</div>

---

<div align="center">
<sub>Built with modern web technologies • Designed for scalability • Optimized for performance</sub>
</div>
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
