# 📌 Django Marksheet Management & Student Auto-Fill System

![Project Banner](path/to/your/banner-image.png)

## 📖 Overview

The **Django Marksheet Management & Student Auto-Fill System** is a web-based application that streamlines the process of filling student details and generating marksheets.

### 🔹 Key Features

- **CAPTCHA-based Auto-Fill**: Users enter a CAPTCHA manually, and the system fetches student details using live web scraping.
- **Marksheet Generation**: Displays semester results, subject achievements, and predicts CGPA.
- **Data Storage & Visualization**: Maintains a secure database with analytics dashboards.
- **Simple Deployment**: Hosted on an Ubuntu server for efficient and cost-effective management.

## 🚀 Features

✅ **Manual CAPTCHA Entry & Auto-Fill**
- Users enter a CAPTCHA, and the system extracts student details via web scraping.
- Uses **Selenium & BeautifulSoup** for automation.

✅ **Comprehensive Marksheet Generation**
- Displays **semester-wise scores, top subjects, and CGPA predictions**.
- Provides insights into **best and weak subjects**.

✅ **Data Storage & Visualization**
- Stores student records in a **secure online database**.
- **Graphical analytics dashboard** using **Matplotlib & Plotly**.
- Supports **exporting reports** for academic analysis.

✅ **User Authentication & Security**
- **Admin authentication system** for secure data management.
- **User-friendly interface** for teachers and administrators.

✅ **Easy Deployment**
- **Runs on Ubuntu server** without Nginx, ensuring hassle-free maintenance.

## 🛠️ Tech Stack

| Technology       | Description |
|-----------------|------------|
| **Django**      | Backend framework for handling logic & authentication. |
| **Python (Selenium, BeautifulSoup)** | Used for scraping student details from external sources. |
| **HTML, CSS, JavaScript (Bootstrap)** | Frontend UI for an intuitive user experience. |
| **SQLite / PostgreSQL** | Stores student data & marksheets. |
| **Matplotlib, Plotly** | Data visualization & analytics dashboard. |
| **Ubuntu Server** | Deployment platform for cost-effective hosting. |

## 📂 Project Structure

```
📂 Django-Marksheet-System
│── 📂 app/                  # Core application logic
│── 📂 models/               # Database models
│── 📂 utils/                # Web scraping logic
│── 📂 scripts/              # Testing & deployment scripts
│── 📂 templates/            # HTML templates
│── 📂 static/               # CSS, JavaScript, images
│── 📜 requirements.txt      # Dependencies
│── 📜 README.md             # Documentation
│── 📜 manage.py             # Django project entry point
```

## 📥 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/priyans877/Django-Marksheet-System.git
cd Django-Marksheet-System
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run Database Migrations
```bash
python manage.py migrate
```

### 5️⃣ Start the Server
```bash
python manage.py runserver
```
✅ **Now, open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser!**

## 🖥️ Usage Guide

1️⃣ **Login to Admin Panel**
- Visit `/admin`, log in as a teacher/admin.
- Manage student records and review marksheets.

2️⃣ **Enter CAPTCHA & Fetch Student Details**
- Input CAPTCHA manually.
- System scrapes **name, roll number, and course details**.

3️⃣ **Generate Marksheet & Insights**
- View **semester results, CGPA prediction, & top subjects**.
- Identify strengths & improvement areas.

4️⃣ **Data Visualization Dashboard**
- View **graphs & analytics** for student performance trends.

## 📸 Screenshots & Demo

| Feature | Screenshot |
|---------|-----------|
| **Login Page** | ![Login](path/to/login-image.png) |
| **CAPTCHA Entry & Auto-Fill** | ![CAPTCHA](path/to/captcha-image.png) |
| **Marksheet Generation** | ![Marksheet](path/to/marksheet-image.png) |
| **Data Visualization Dashboard** | ![Dashboard](path/to/dashboard-image.png) |

## 🚀 Deployment on Ubuntu Server

### 1️⃣ Install Required Dependencies
```bash
sudo apt update && sudo apt install python3-pip python3-venv
```

### 2️⃣ Clone the Repository
```bash
git clone https://github.com/priyans877/Django-Marksheet-System.git
cd Django-Marksheet-System
```

### 3️⃣ Setup Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 5️⃣ Run Migrations & Start Server
```bash
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```
🎉 **Your project is now live on the server!**

## 🛠 Troubleshooting

🔹 **Database Errors**
```bash
python manage.py makemigrations
python manage.py migrate
```

🔹 **Selenium Not Working?**
Ensure **Google Chrome & ChromeDriver** are installed correctly.

🔹 **Forgot Admin Credentials?**
```bash
python manage.py createsuperuser
```
Then follow the prompts to create a new admin user.

## 🎯 Future Roadmap

✔️ **PDF Export for Marksheet Reports**
✔️ **AI-based Student Performance Prediction**
✔️ **Mobile-Friendly UI**
✔️ **Integration with School Databases**

## 🤝 Contributors

👤 **Priyanshu Choubey**  
- **GitHub**: [@priyans877](https://github.com/priyans877)  
- **LinkedIn**: [Priyanshu Choubey](https://www.linkedin.com/in/priyanshu-choubey/)  

🙌 **Contributions are welcome!** Feel free to **submit a pull request** or raise an issue.

## 📜 License
This project is licensed under the **MIT License**. See `LICENSE` for details.

## ⭐ Final Thoughts
🚀 This project **simplifies student data management** by automating **detail fetching and marksheet generation**.  
💡 If you **find this useful, don't forget to ⭐ star the repo on GitHub!**

