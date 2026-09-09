<div class="hero">

<h1>🎓 Student Academic Information System (SI-MAS)</h1>

<p>Academic Administration · Course Registration · Student Records · Role-Based Access</p>

<p>
  <img src="https://img.shields.io/badge/Laravel-FF2D20?style=flat-square&logo=laravel&logoColor=white" alt="Laravel"/>
  <img src="https://img.shields.io/badge/PHP-777BB4?style=flat-square&logo=php&logoColor=white" alt="PHP"/>
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white" alt="MySQL"/>
  <img src="https://img.shields.io/badge/Bootstrap-7952B3?style=flat-square&logo=bootstrap&logoColor=white" alt="Bootstrap"/>
  <img src="https://img.shields.io/badge/Web%20Application-6D28D9?style=flat-square" alt="Web Application"/>
  <img src="https://img.shields.io/badge/Role--Based%20Access-8B5CF6?style=flat-square" alt="Role-Based Access"/>
  <img src="https://img.shields.io/badge/License-MIT-22C55E?style=flat-square" alt="MIT License"/>
</p>

<p>
A web-based academic information system designed to streamline course registration,
academic record management, validation workflows, and role-based administrative access.
</p>

<p>
<strong>
<a href="https://bers31.github.io/bernardo.github.io/Student_Academic_Information_System/">🌐 Live Demo</a>
</strong>
&nbsp;·&nbsp;
<strong>
<a href="https://github.com/bers31/bernardo.github.io/tree/main/Student_Academic_Information_System">📁 Repository</a>
</strong>
</p>

</div>

---

## 📖 Project Overview

**SI-MAS (Student Academic Information System)** is an integrated web application designed to support university academic administration.

The system was developed to improve the way students, academic advisors, faculty, and administrators interact with academic information and workflows.

The application focuses on:

* Course registration.
* Academic record access.
* Academic data validation.
* Administrative workflows.
* Role-based access control.
* Academic performance management.
* Responsive web interaction.

The platform was designed to support a large academic user base, serving **1,000+ students and 100 academic advisors**, while also supporting data workflows involving more than **100 faculty members**.

```text id="m7x3q8"
Students / Faculty / Advisors / Administrators
                    ↓
              Authentication
                    ↓
            Role Identification
                    ↓
          Academic Application
                    ↓
       ┌────────────┼────────────┐
       ↓            ↓            ↓
Course Registration  Records   Academic Processes
       │            │            │
       └────────────┼────────────┘
                    ↓
              MySQL Database
```

> **Portfolio focus:** This project demonstrates full-stack web application development with Laravel, relational database management, academic workflow automation, data validation, secure authorization, usability testing, and stakeholder-oriented system design.

---

## 🎯 Project Objectives

The project was developed around several operational objectives:

1. Streamline student course-registration workflows.
2. Provide centralized access to academic records.
3. Reduce manual administrative effort.
4. Improve academic data accuracy through automated validation.
5. Provide secure, role-aware access to academic information.
6. Support faculty and academic advisors in administrative workflows.
7. Improve usability through iterative user testing.
8. Document the system for administrators and future maintenance.

---

## 📊 Scale & Impact

The system was designed to support a substantial academic user environment.

| Metric                               | Project Impact                              |
| ------------------------------------ | ------------------------------------------- |
| 👨‍🎓 **Students**                   | **1,000+**                                  |
| 👨‍🏫 **Academic Advisors**          | **100**                                     |
| 🏛️ **Faculty Members**              | **100+**                                    |
| ⏱️ **Registration Time Improvement** | **30% reduction**                           |
| 🔐 **Access Model**                  | Role-based authentication and authorization |

The scale emphasizes that SI-MAS was not designed merely as a small CRUD demonstration, but as a structured academic administration application.

---

## 👥 User Roles

The system provides role-aware functionality for different academic stakeholders.

### 🎓 Students

Students can use the system for:

* Course registration.
* Academic record access.
* Schedule checking.
* Academic progress monitoring.
* Viewing relevant academic information.

### 👨‍🏫 Academic Advisors

Academic advisors can support student academic processes through:

* Registration review.
* Academic advising workflows.
* Student academic monitoring.
* Approval-related activities.

### 🏛️ Faculty & Academic Administration

Faculty-facing functionality supports academic processes such as:

* Academic data management.
* Grading-related workflows.
* Attendance management.
* Performance monitoring.

### 🔧 Administrators

Administrative users can manage system-level academic data and maintain application records.

The general access model is:

```text id="c8q5m2"
                    User
                     ↓
               Authentication
                     ↓
              Role Identification
                     ↓
       ┌─────────────┼─────────────┐
       ↓             ↓             ↓
    Student       Advisor       Faculty/Admin
       ↓             ↓             ↓
  Student Area   Academic       Administrative
                 Workflow          Area
```

---

## 🔐 Authentication & Authorization

Security is a core component because the application handles academic information.

The system provides:

* Authentication.
* Role-based authorization.
* Protected application areas.
* Controlled access to academic information.
* Session-aware user interaction.
* Data privacy protection.

Conceptually:

```text id="w4m8x2"
Login
  ↓
Identity Verification
  ↓
Role Detection
  ↓
Permission Check
  ↓
Authorized Dashboard
```

This prevents users from accessing functionality outside the responsibilities associated with their role.

---

## 📝 Course Registration Workflow

Course registration is one of the central workflows of SI-MAS.

The process can be summarized as:

```text id="p7m3x9"
Student
  ↓
Select Courses
  ↓
Submit Registration
  ↓
Automated Validation
  ↓
Advisor Review / Approval
  ↓
Confirmed Registration
  ↓
Academic Record
```

The system reduces administrative friction by replacing repetitive manual processing with a structured digital workflow.

This contributed to a **30% reduction in the average time required for course registration**.

---

## ✅ Automated Data Validation

Academic systems require consistent and accurate records.

SI-MAS incorporates automated validation to reduce:

* Manual input errors.
* Inconsistent academic records.
* Invalid registration states.
* Repetitive administrative checking.

The validation workflow is:

```text id="x5q8m4"
Input
  ↓
Validation Rules
  ↓
Consistency Check
  ↓
Valid ───────→ Save / Process
  │
  └──────────→ Reject / Correct
```

This helps reduce faculty workload while improving the reliability of academic data.

---

## 📚 Academic Record Management

The system centralizes important academic information.

Typical academic records include:

* Course registrations.
* Course schedules.
* Grades.
* Academic history.
* Student progress.
* Performance-related information.

The general information flow is:

```text id="n6m2q7"
Academic Activity
       ↓
Application Processing
       ↓
Validated Record
       ↓
MySQL Persistence
       ↓
Role-Specific Access
```

This creates a single application environment for accessing relevant academic information.

---

## 📈 Academic Performance Analytics

The platform supports academic performance-oriented functionality, allowing faculty and academic stakeholders to work with student performance information.

Potential analytical areas include:

* Grade records.
* Course performance.
* Academic progress.
* Attendance-related information.
* Student performance monitoring.

This extends SI-MAS beyond simple registration into a broader academic information environment.

---

## 🕐 Schedule & Academic Activity Management

Academic scheduling is another important workflow.

The system organizes information related to:

* Courses.
* Class schedules.
* Academic activities.
* Faculty assignments.
* Student-facing schedule access.

The workflow is:

```text id="r8m4x1"
Course / Academic Activity
          ↓
Schedule Management
          ↓
Academic Database
          ↓
Faculty / Student Access
```

Centralized schedule management helps reduce inconsistencies between administrative and student-facing information.

---

## 🤝 Faculty Collaboration

The system was refined through collaboration with faculty to accommodate academic requirements that differ from one workflow to another.

This collaboration helped shape functionality related to:

* Academic administration.
* Automated grading workflows.
* Attendance tracking.
* Performance analytics.
* Role-specific system behavior.

The development process therefore combined technical implementation with domain feedback.

```text id="q4m7x2"
Technical Implementation
          +
Faculty Requirements
          ↓
Workflow Refinement
          ↓
More Relevant Academic System
```

---

## 🧪 User Testing & Iterative Improvement

User testing was conducted to gather feedback from system users and identify usability issues.

The refinement cycle was:

```text id="v7m3k8"
Initial Implementation
        ↓
User Testing
        ↓
Collect Feedback
        ↓
Identify Usability Issues
        ↓
Iterative Update
        ↓
Improved Experience
```

Attention was given to:

* Workflow simplicity.
* Information accessibility.
* Dashboard usability.
* Registration experience.
* Role-specific interaction.

This user-centered approach contributed to improved overall system usability.

---

## 🗄️ Database Architecture

The system uses **MySQL** as its relational database layer.

The database is responsible for storing structured academic information.

Conceptually:

```text id="m5x8q3"
Users
  │
  ├── Students
  ├── Advisors
  ├── Faculty
  └── Administrators
          │
          ↓
      Academic Data
          │
     ┌────┼────┐
     ↓    ↓    ↓
  Courses Schedules Grades
     │    │    │
     └────┼────┘
          ↓
    Academic Records
```

The relational model supports consistency between users, academic activities, and student records.

---

## 🔄 Data Management Workflow

The application follows a structured lifecycle for academic information:

```text id="z6q4m8"
Create
  ↓
Validate
  ↓
Process
  ↓
Store
  ↓
Retrieve
  ↓
Display
  ↓
Update
```

Laravel handles application-level processing while MySQL provides persistent data storage.

---

## ⚙️ Laravel Application Architecture

Laravel provides the primary web application framework.

The architecture follows a structured separation between application responsibilities:

```text id="k3m8p5"
HTTP Request
     ↓
Laravel Routing
     ↓
Controller / Application Logic
     ↓
Validation
     ↓
Database Interaction
     ↓
Response / View
```

This provides a maintainable foundation for the academic workflows managed by SI-MAS.

---

## 🌐 Web Application Interface

The interface is designed to provide a consistent experience across different academic roles.

**Bootstrap** supports the responsive presentation layer, helping the application adapt across different screen sizes.

The interface emphasizes:

* Clear navigation.
* Role-specific dashboards.
* Structured academic information.
* Accessible forms.
* Responsive layouts.
* Consistent interaction patterns.

---

## 📋 Core Academic Modules

| Module                         | Function                                       |
| ------------------------------ | ---------------------------------------------- |
| 👨‍🎓 **Student Portal**       | Course registration and academic record access |
| 📝 **Registration Management** | Structured course registration workflow        |
| 📚 **Academic Records**        | Access to grades and academic history          |
| 🗓️ **Schedule Management**    | Manage and access academic schedules           |
| ✅ **Data Validation**          | Automated checking of academic input           |
| 👨‍🏫 **Advisor Workflow**     | Support academic review and advising           |
| 📈 **Performance Analytics**   | Monitor student academic performance           |
| 🔐 **Authentication & RBAC**   | Secure role-specific application access        |
| 🔧 **Administration**          | Manage academic and system-level data          |

---

## 🏗️ System Architecture

SI-MAS can be understood through four primary layers.

### 🌐 Presentation Layer

```text id="f4m8q2"
Bootstrap-Based Web Interface
            ↓
Role-Specific Dashboard
            ↓
Student / Advisor / Faculty / Admin Views
```

### ⚙️ Application Layer

```text id="x7p3m5"
Laravel + PHP
      ↓
Routing
      ↓
Business Logic
      ↓
Validation
      ↓
Authorization
```

### 🗄️ Data Layer

```text id="r5m8q4"
MySQL
   ↓
Users
Courses
Schedules
Grades
Academic Records
```

### 🔐 Security Layer

```text id="n3q7x8"
Authentication
      +
Authorization
      +
Role-Based Access
      +
Data Privacy
```

---

## 🔄 End-to-End System Flow

```text id="p8m4q2"
┌──────────────────────┐
│ Academic User        │
│ Student / Faculty    │
│ Advisor / Admin      │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Authentication       │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Role-Based Access    │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Laravel Application  │
│ PHP + Bootstrap      │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Validation &         │
│ Academic Processing  │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ MySQL Database       │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Academic Dashboard   │
│ / Records / Reports  │
└──────────────────────┘
```

---

## 📊 Operational Impact

The project delivered measurable process improvements.

### ⏱️ Faster Course Registration

The redesigned registration workflow reduced the average registration time by **30%**.

```text id="c5m8q1"
Traditional Workflow
        ↓
Manual Processing
        ↓
Longer Registration Time

SI-MAS Workflow
        ↓
Digital Registration
        ↓
Automated Validation
        ↓
Faster Approval
        ↓
30% Time Reduction
```

### 🧹 Lower Manual Workload

Automated validation reduces repetitive administrative checking and helps minimize human error.

### 🔎 Better Data Accessibility

Students and academic staff can access relevant academic information through centralized web interfaces.

---

## 💼 Business & Institutional Value

SI-MAS creates value through several interconnected improvements:

| Area                           | Value                                                     |
| ------------------------------ | --------------------------------------------------------- |
| ⏱️ **Efficiency**              | Faster academic registration and processing               |
| ✅ **Accuracy**                 | Automated validation reduces manual errors                |
| 🔐 **Security**                | Role-aware access protects academic information           |
| 📚 **Accessibility**           | Centralized academic information is easier to access      |
| 🎓 **Student Experience**      | Simplified registration and academic-record access        |
| 👨‍🏫 **Faculty Productivity** | Reduced repetitive administrative work                    |
| 📈 **Academic Monitoring**     | Performance and attendance information support monitoring |

---

## 🧩 Problem-to-Solution Mapping

| Problem                          | SI-MAS Response                             |
| -------------------------------- | ------------------------------------------- |
| Manual course registration       | Digital registration workflow               |
| Repetitive validation            | Automated data validation                   |
| Fragmented academic information  | Centralized academic system                 |
| Unauthorized access              | Authentication and role-based authorization |
| Difficult academic monitoring    | Centralized performance information         |
| Usability issues                 | User testing and iterative refinement       |
| Complex administrative workflows | Role-specific functionality                 |

---

## 🛠️ Technology Stack

| Layer                        | Technology                          | Purpose                                                     |
| ---------------------------- | ----------------------------------- | ----------------------------------------------------------- |
| 🌐 **Application Framework** | **Laravel**                         | Core web application framework                              |
| 🐘 **Programming Language**  | **PHP**                             | Server-side application logic                               |
| 🗄️ **Database**             | **MySQL**                           | Relational academic data storage                            |
| 🎨 **Frontend Framework**    | **Bootstrap**                       | Responsive interface and UI layout                          |
| 🔐 **Security**              | **Authentication & Authorization**  | Protect academic functionality and information              |
| 📊 **Application Domain**    | **Academic Information Management** | Registration, records, schedules, and performance workflows |

---

## 🔬 Technical Highlights

### Laravel-Based Web Application

Laravel provides the foundation for academic workflows, data processing, routing, and application logic.

### Relational Data Management

MySQL provides structured persistence for academic data and relationships between students, faculty, courses, schedules, and records.

### Automated Validation

Validation logic reduces manual checking and improves data consistency.

### Role-Based Authorization

Different academic users receive functionality appropriate to their role.

### Responsive UI

Bootstrap supports a consistent interface across desktop and mobile screen sizes.

### User-Centered Iteration

User testing and faculty collaboration are incorporated into the development process.

---

## 🗺️ Project Scope

| Module                                | Description                                         | Status        |
| ------------------------------------- | --------------------------------------------------- | ------------- |
| 🎓 **Student Information Management** | Centralized student academic information            | ✅ Implemented |
| 📝 **Course Registration**            | Digital registration and approval workflow          | ✅ Implemented |
| ✅ **Automated Validation**            | Input and academic-data validation                  | ✅ Implemented |
| 📚 **Academic Records**               | Grades and academic history access                  | ✅ Implemented |
| 🗓️ **Schedule Management**           | Academic scheduling and information access          | ✅ Implemented |
| 👨‍🏫 **Advisor Workflow**            | Academic advising and review processes              | ✅ Implemented |
| 📈 **Performance Analytics**          | Academic performance monitoring                     | ✅ Implemented |
| 👥 **Multi-Role Access**              | Student, advisor, faculty, and administrator access | ✅ Implemented |
| 🔐 **Authentication & Authorization** | Secure academic information access                  | ✅ Implemented |
| 🎨 **Responsive Interface**           | Bootstrap-based responsive web UI                   | ✅ Implemented |
| 🧪 **User Testing**                   | Feedback-driven iterative improvements              | ✅ Applied     |
| 🤝 **Faculty Collaboration**          | Feature refinement based on academic requirements   | ✅ Applied     |
| 📖 **Documentation**                  | Development and user documentation                  | ✅ Implemented |

---

## 📈 Portfolio Alignment

The project directly reflects the capabilities described in the professional project entry:

| LinkedIn Capability       | Project Evidence                    |
| ------------------------- | ----------------------------------- |
| Laravel                   | Core web application framework      |
| MySQL                     | Academic data persistence           |
| PHP                       | Server-side application development |
| Bootstrap                 | Responsive UI                       |
| 1,000+ students           | Large academic user base            |
| 100 academic advisors     | Advisor workflow support            |
| 100+ faculty members      | Faculty-oriented data processes     |
| 30% faster registration   | Measured workflow improvement       |
| Automated data validation | Reduced manual error and workload   |
| User testing              | Iterative UX refinement             |
| Secure authentication     | Protected academic information      |
| Authorization             | Role-based application access       |
| Faculty collaboration     | Domain-driven feature refinement    |
| Grading                   | Academic record workflow            |
| Attendance tracking       | Academic activity monitoring        |
| Performance analytics     | Student performance monitoring      |
| Documentation             | User guides and technical handover  |

> **Portfolio positioning:** This project demonstrates the ability to build a multi-role academic information platform that combines transactional workflows, relational data management, automation, security, usability, and stakeholder collaboration.

---

## 🧪 Testing & Quality Assurance

The system was evaluated across key academic workflows.

### Functional Areas

* Authentication and logout.
* Role-specific dashboard access.
* Course registration.
* Data validation.
* Academic record access.
* Schedule management.
* Academic workflow interactions.
* User-facing usability.

### Iterative Testing

```text id="q8m4x5"
Feature
 ↓
User Testing
 ↓
Feedback
 ↓
Bug / Usability Identification
 ↓
Implementation Update
 ↓
Re-Test
```

This approach ensures that the system evolves according to actual user needs rather than purely technical assumptions.

---

## 📖 Documentation & Handover

The development process was documented to support:

* Technical understanding.
* Administrative handover.
* Future maintenance.
* User onboarding.
* Continued system development.

User guides help reduce the learning curve for new administrators and users.

---

## 🎥 Demo & Screenshots

### 🌐 Live Demo

<div align="center">

<p>
<a href="https://bers31.github.io/bernardo.github.io/Student_Academic_Information_System/">
<strong>🔗 View SI-MAS Live Demo</strong>
</a>
</p>

</div>

### 🏠 Dashboard Overview

![Dashboard Overview](images/Picture14.png)

*Academic system dashboard providing access to role-specific functionality.*

### 📋 Student Registration

![Course Registration](images/Picture.png)

*Course-registration workflow for student academic administration.*

### 📊 Academic Interface

![Academic Interface](images/Picture1.png)

*Academic information and workflow interface.*

---

## 📸 Full Screenshots

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

---

## 🔭 Future Development

Potential future improvements include:

* More granular academic analytics.
* Automated academic notifications.
* Expanded student-performance dashboards.
* More advanced approval workflows.
* Mobile-focused interfaces.
* Improved administrative reporting.
* Expanded integration with university systems.
* More comprehensive audit and monitoring capabilities.

These are potential extensions and are not presented as current functionality unless implemented in the repository.

---

## 📄 License

This project is licensed under the **MIT License** — see the [`LICENSE`](LICENSE) file for the complete license text.

Third-party libraries, frameworks, datasets, and other external components remain subject to their respective licenses and terms.

---

<div class="contact-hero">

<p><strong>Interested in the project?</strong></p>

<p>
👨‍💻 <strong>Bernardo Nandaniar Sunia</strong><br/>
Bachelor of Computer Science — Diponegoro University<br/>
Laravel · MySQL · PHP · Bootstrap · Academic Information Systems
</p>

<p>
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

<p>
<em>Academic Systems · Web Development · Data Management · Workflow Automation</em>
</p>

</div>

---

## 📌 Conclusion

**SI-MAS** demonstrates the development of a structured academic information system using **Laravel, PHP, MySQL, and Bootstrap** to simplify university administration and improve accessibility to academic information.

The platform supports **1,000+ students, 100 academic advisors, and more than 100 faculty members**, while incorporating automated data validation, role-based authentication and authorization, academic records, registration workflows, scheduling, grading, attendance, and performance-oriented functionality.

A measurable outcome of the project was a **30% reduction in average course-registration time**, supported by digital workflows and automated validation that reduced repetitive administrative work and minimized human error.

Through user testing, faculty collaboration, and comprehensive documentation, the project demonstrates not only the implementation of a web application, but also the ability to develop a system around real academic workflows, user requirements, operational efficiency, security, and long-term maintainability.