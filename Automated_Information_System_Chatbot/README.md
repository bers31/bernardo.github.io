<div align="center">
  <h1>🏛️ 
Automated “Information Center” Chatbot for Class II Ambarawa Correctional Facility </h1>
  <em>Intelligent Communication Platform for Modern Correctional Management</em>
</div>

<div align="center">
  <img src="https://img.shields.io/badge/python-v3.8+-blue.svg" alt="Python"/>
  <img src="https://img.shields.io/badge/flask-v2.3.0-green.svg" alt="Flask"/>
  <img src="https://img.shields.io/badge/OpenAI-API-orange.svg" alt="OpenAI API"/>
  <img src="https://img.shields.io/badge/license-MIT-brightgreen.svg" alt="License"/>
  <img src="https://img.shields.io/badge/build-passing-success.svg" alt="Build Status"/>
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version"/>
  <img src="https://img.shields.io/badge/PWA-Ready-purple.svg" alt="PWA Ready"/>
</div>

---

## 📖 **Project Overview**

The **Prison Chatbot System** is a cutting-edge Progressive Web Application designed specifically for **Lapas Kelas II A Ambarawa Correctional Facility**. This intelligent platform revolutionizes communication between inmates and staff by providing a secure, AI-powered chatbot interface alongside a comprehensive administrative dashboard.

Built with modern web technologies and powered by OpenAI's advanced natural language processing, this system addresses the critical need for efficient, scalable communication management in correctional facilities while maintaining the highest security standards.

**Why This Matters:**
- Streamlines administrative communication processes
- Reduces staff workload through intelligent automation
- Provides 24/7 support for inmate inquiries
- Enhances operational transparency and efficiency
- Implements modern digital solutions in correctional management

---

<table>
  <tr>
    <td width="50%">
      <h3>🤖 Intelligent Chat System</h3>
      <ul>
        <li>OpenAI-powered natural language understanding</li>
        <li>Context-aware conversation management</li>
        <li>Multi-language support capabilities</li>
        <li>Intent detection and response generation</li>
      </ul>
      <h3>🔒 Enterprise Security</h3>
      <ul>
        <li>Advanced authentication &amp; session management</li>
        <li>Password hashing with Werkzeug Security</li>
        <li>CSRF protection and rate limiting</li>
        <li>Secure admin access controls</li>
      </ul>
      <h3>📱 Progressive Web App</h3>
      <ul>
        <li>Offline functionality with service workers</li>
        <li>Cross-platform compatibility</li>
        <li>App-like user experience</li>
        <li>Asset caching for optimal performance</li>
      </ul>
    </td>
    <td width="50%">
      <h3>📊 Admin Dashboard</h3>
      <ul>
        <li>Real-time chat monitoring</li>
        <li>User management system</li>
        <li>System health analytics</li>
        <li>Conversation logs visualization</li>
      </ul>
      <h3>📧 Communication Suite</h3>
      <ul>
        <li>Email notification system</li>
        <li>Web push notifications</li>
        <li>Password reset workflows</li>
        <li>Real-time alerts</li>
      </ul>
      <h3>🗄️ Data Management</h3>
      <ul>
        <li>SQLite database integration</li>
        <li>Automated data migration</li>
        <li>CRUD operations for all entities</li>
        <li>Secure data persistence</li>
      </ul>
    </td>
  </tr>
</table>

---

<h2>🛠️ Technology Stack &amp; Tools</h2>
<div align="center">
  <table>
    <tr><th>Category</th><th>Technologies</th></tr>
    <tr>
      <td>Backend Framework</td>
      <td>
        <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/>
        <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/>
      </td>
    </tr>
    <tr>
      <td>Database</td>
      <td><img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white"/></td>
    </tr>
    <tr>
      <td>AI/ML</td>
      <td><img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white"/></td>
    </tr>
    <tr>
      <td>Frontend</td>
      <td>
        <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/>
        <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white"/>
        <img src="https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E"/>
      </td>
    </tr>
    <tr>
      <td>Security</td>
      <td>
        <img src="https://img.shields.io/badge/Werkzeug-FF6B6B?style=for-the-badge"/>
        <img src="https://img.shields.io/badge/CORS-4CAF50?style=for-the-badge"/>
      </td>
    </tr>
    <tr>
      <td>Deployment</td>
      <td><img src="https://img.shields.io/badge/GitHub%20Pages-222222?style=for-the-badge&logo=GitHub%20Pages&logoColor=white"/></td>
    </tr>
  </table>
</div>

<h3>Core Dependencies:</h3>
<pre><code>Flask==2.3.0
Flask-Mail==0.9.1
Flask-Limiter==3.5.0
Flask-CORS==4.0.0
openai==0.28.0
pywebpush==1.14.0
Werkzeug==2.3.0
</code></pre>

---

## 🚀 **Installation & Setup**

### **Prerequisites**
- Python 3.8+ installed
- Git for version control
- OpenAI API key
- SMTP email credentials (for notifications)

### **Quick Start**

```bash
# 1. Clone the repository
git clone https://github.com/bers31/bernardo.github.io.git
cd bernardo.github.io

# 2. Create virtual environment
python -m venv prison_chatbot_env
source prison_chatbot_env/bin/activate  # On Windows: prison_chatbot_env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your configuration:
# OPENAI_API_KEY=your_openai_api_key
# SMTP_SERVER=your_smtp_server
# SMTP_USERNAME=your_email
# SMTP_PASSWORD=your_password

# 5. Initialize database
python -c "from backend import init_db; init_db()"

# 6. Run the application
python backend.py
```

### **Docker Deployment** (Optional)
```bash
# Build and run with Docker
docker build -t prison-chatbot .
docker run -p 5000:5000 --env-file .env prison-chatbot
```

**🌐 Access Points:**
- **Main Application:** `http://localhost:5000`
- **Admin Dashboard:** `http://localhost:5000/admin_login.html`
- **API Endpoints:** `http://localhost:5000/api/`

---

<h2>🎥 Demo </h2>
<div align="center">
  <p><strong>🖥️ Live Demo</strong></p>
  <p><a href="https://bers31.github.io/bernardo.github.io/Automated_Information_System_Chatbot/">🔗 Visit Live Application</a></p>
</div>

<table>
  <tr>
    <td width="33%">
      <img src="https://bers31.github.io/bernardo.github.io/Automated_Information_System_Chatbot/images/Picture6.png" alt="Chat Interface" width="100%"/>
      <p align="center"><strong>User Chat Interface</strong><br/>Clean, intuitive design for easy communication</p>
    </td>
    <td width="33%">
      <img src="https://bers31.github.io/bernardo.github.io/Automated_Information_System_Chatbot/images/Picture1.png" alt="Admin Login" width="100%"/>
      <p align="center"><strong>Admin Login</strong><br/>Secure access gateway for system administrators</p>
    </td>
    <td width="33%">
      <img src="https://bers31.github.io/bernardo.github.io/Automated_Information_System_Chatbot/images/Picture3.png" alt="Admin Dashboard" width="100%"/>
      <p align="center"><strong>Admin Dashboard</strong><br/>Comprehensive management and monitoring</p>
    </td>
  </tr>
</table>

### **📱 Progressive Web App Features**
- ✅ **Offline Functionality** - Works without internet connection
- ✅ **App Installation** - Can be installed on any device
- ✅ **Push Notifications** - Real-time updates and alerts
- ✅ **Responsive Design** - Optimized for all screen sizes

---

<h2>🗺️ Project Roadmap</h2>
<div align="center">
  <table>
    <tr><th>Milestone</th><th>Features</th><th>Target Date</th><th>Status</th></tr>
    <tr><td>Phase 1</td><td>Core chatbot functionality, basic admin panel</td><td>Q1 2025</td><td>✅ Complete</td></tr>
    <tr><td>Phase 2</td><td>PWA implementation, offline support</td><td>Q2 2025</td><td>✅ Complete</td></tr>
    <tr><td>Phase 3</td><td>Advanced analytics, reporting dashboard</td><td>Q3 2025</td><td>🚧 In Progress</td></tr>
    <tr><td>Phase 4</td><td>Multi-language support, voice integration</td><td>Q4 2026</td><td>📋 Planned</td></tr>
    <tr><td>Phase 5</td><td>Mobile app deployment, advanced AI features</td><td>Q5 2027</td><td>📋 Planned</td></tr>
  </table>
</div>

---

<h2>🏗️ System Architecture</h2>
<pre><code>┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask Backend │    │   External APIs │
│   (PWA)         │◄──►│   (backend.py)  │◄──►│   (OpenAI)      │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • Chat UI       │    │ • Route Handler │    │ • NLP Processing│
│ • Admin Panel   │    │ • Session Mgmt  │    │ • Email Service │
│ • Service Worker│    │ • Database ORM  │    │ • Push Notifications│
│ • PWA Manifest  │    │ • Security Layer│    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   SQLite DB     │
                    │                 │
                    │ • Users         │
                    │ • Messages      │
                    │ • Chat Logs     │
                    │ • Admin Settings│
                    └─────────────────┘
</code></pre>

---

## 🤝 **Contributing**

We welcome contributions from the developer community! Here's how you can help:

### **Getting Started**
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### **Contribution Guidelines**
- Follow PEP 8 style guide for Python code
- Add unit tests for new features
- Update documentation for any API changes
- Ensure all tests pass before submitting PR

---

## 🧪 **Testing**

```bash
# Run unit tests
python -m pytest tests/

# Run with coverage report
python -m pytest --cov=backend tests/

# Run integration tests
python -m pytest tests/integration/

# Performance testing
python -m pytest tests/performance/
```

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

**🔐 Security Notice:** This system handles sensitive correctional facility data. Please ensure proper security configurations and compliance with relevant regulations before deployment in production environments.
   
### Full Screenshots
![Screenshot 1](images/Picture1.png)
![Screenshot 2](images/Picture2.png)
![Screenshot 3](images/Picture3.png)
![Screenshot 4](images/Picture4.png)
![Screenshot 5](images/Picture5.png)
![Screenshot 6](images/Picture6.png)

### Conclusion
This project delivers a full-spectrum AI‑driven chatbot solution, seamlessly blending intuitive front‑end interactions with a robust, scalable backend. From advanced NLP‑powered dialogue management and secure data handling to dynamic notification workflows and analytics‑ready logging, it empowers organizations to automate information delivery, elevate user engagement, and extract actionable insights. Ready for production deployment, this end‑to‑end chatbot architecture transforms how users access and interact with essential services and knowledge.
