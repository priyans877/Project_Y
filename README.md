Aravali DashBoard & Marksheet System 🏫🎓


📌 Overview
The Django AutoCAPTCHA & Marksheet System is an intelligent web application that streamlines the student details entry process by automatically filling them using live web scraping. It also features a marksheet generation system that provides detailed academic insights, including semester results, top subject achievements, and expected CGPA calculations.

The system aims to eliminate manual errors, save time, and provide valuable academic analytics. It is a cost-effective and lightweight solution, deployed on a simple Ubuntu server.

🎯 Key Features
✅ Automated Student Detail Retrieval
Enter a CAPTCHA code, and the system scrapes student details from an external database in real time.
Uses Selenium and BeautifulSoup for web automation.
✅ Marksheet Generator
Displays semester-wise scores and subject performance insights.
Automatically predicts missing CGPA based on past scores.
Highlights top-performing subjects and areas for improvement.
✅ Data Storage & Visualization
Stores student details in an online database.
Graphical dashboards to analyze student performance.
Supports data export and reports generation.
✅ Secure & User-Friendly
Admin authentication system for security.
Simple UI designed for teachers and admins.
Deployed on an Ubuntu server without Nginx, ensuring easy maintenance.
🛠️ Technology Stack
Technology	Description
Django	Backend framework for handling authentication, database operations, and logic.
Python (BeautifulSoup, Selenium)	Used for live web scraping to fetch student details.
HTML, CSS, JavaScript (Bootstrap)	Frontend for building a user-friendly UI.
SQLite / PostgreSQL	Database for storing student information and marksheets.
Matplotlib, Plotly	Data visualization for student performance analysis.
Ubuntu Server	Deployment platform for cost-effective hosting.
🚀 Project Architecture
php
Copy
Edit
📂 Django-AutoCAPTCHA
│── 📂 app/                  # Main application logic
│── 📂 models/               # Database models
│── 📂 utils/                # CAPTCHA handling & scraping logic
│── 📂 scripts/              # Testing and deployment scripts
│── 📂 templates/            # Frontend templates
│── 📂 static/               # CSS, JavaScript, images
│── 📜 requirements.txt      # Required dependencies
│── 📜 README.md             # Project documentation
│── 📜 manage.py             # Django project entry point
📥 Installation & Setup
Follow these steps to set up the project on your local machine:

1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/priyans877/Django-AutoCAPTCHA.git
cd Django-AutoCAPTCHA
2️⃣ Create a Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
3️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Run Database Migrations
bash
Copy
Edit
python manage.py migrate
5️⃣ Start the Server
bash
Copy
Edit
python manage.py runserver
🚀 Now, open http://127.0.0.1:8000/ in your browser!

🖥️ Usage Guide
1️⃣ Login to Admin Dashboard
Visit /admin to log in as a teacher or admin.
Manage student details and view previous marksheets.
2️⃣ Auto-Fill Student Details
Enter the CAPTCHA code, and the system will fetch student details automatically.
3️⃣ Generate Marksheet
View semester-wise results and top-performing subjects.
Predict CGPA if it is missing.
4️⃣ Visualize Data
Use the dashboard to analyze student performance trends.
📸 Screenshots & Demo
🔹 Login Page

🔹 CAPTCHA Input & Auto-Fill

🔹 Marksheet Generation

🔹 Data Visualization Dashboard

🚀 Deployment
🔹 Running on Ubuntu Server
bash
Copy
Edit
# Install required dependencies
sudo apt update && sudo apt install python3-pip python3-venv

# Clone the repository
git clone https://github.com/priyans877/Django-AutoCAPTCHA.git
cd Django-AutoCAPTCHA

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Django migrations
python manage.py migrate

# Start the server
python manage.py runserver 0.0.0.0:8000
🎉 Your project is now live on the server!

🛠 Troubleshooting
🔹 Database Errors
bash
Copy
Edit
python manage.py makemigrations
python manage.py migrate
🔹 Selenium Not Working?
Ensure Google Chrome & ChromeDriver are installed correctly.

🔹 Can't Access Admin?
bash
Copy
Edit
python manage.py createsuperuser
Then follow the prompts to create a new admin user.

🎯 Future Roadmap
✔️ PDF Export for Marksheet Reports
✔️ AI-based Student Performance Prediction
✔️ Mobile-Friendly UI
✔️ Integration with School Databases

🤝 Contributors
👤 Priyanshu Choubey

GitHub: @priyans877
LinkedIn: Priyanshu Choubey
🙌 Open to contributions! Feel free to submit a pull request or raise an issue.

📜 License
This project is licensed under the MIT License. See LICENSE for details.

🎯 Final Thoughts
🚀 This project is designed to simplify the student marksheet process with AI-powered automation. It not only saves time but also provides deep academic insights using visual dashboards.

💡 If you like this project, don’t forget to ⭐ star the repository on GitHub!

🎯 Would you like any modifications or enhancements? Let me know! 🚀🔥
