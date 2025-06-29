# 🏥 Hospital Management System API

This is the **backend** of a comprehensive **Hospital Management System** built using **Flask**, **SQLAlchemy**, and **RESTful APIs**. It serves as the foundation for managing core hospital operations such as:

- Patient registration (Inpatient, Outpatient)
- Doctor and Department management
- Appointments and Medical Records tracking

---

## 👨‍👩‍👧‍👦 Built by

This project was collaboratively developed as a **group project** by:

- **Gichuki Natalie**  
- **Kipsang Jesse**  
- **Kihikah Kariuki**

We built this system with a strong emphasis on clean design, separation of concerns, and modularity — laying a scalable foundation for a real-world hospital's digital transformation.

---

## 📦 Tech Stack

| Layer        | Tools Used                      |
|------------- |---------------------------------|
| **Language** | Python 3                        |
| **Framework**| Flask, Flask-RESTful            |
| **ORM**      | SQLAlchemy + Flask-Migrate      |
| **DB**       | SQLite (via SQLAlchemy)         |
| **API Docs** | JSON via Postman                |
| **CORS**     | Flask-CORS                      |

---

## Features

- 🔹 Full **CRUD** for Patients, Doctors, Appointments, Medical Records, and Departments
- 🔹 Supports **Inpatients** and **Outpatients** using inheritance (polymorphic models)
- 🔹 **Head doctor assignment** in departments
- 🔹 Relational integrity between appointments and medical records
- 🔹 Organized using **Blueprints** and **Flask-Restful Resources**
- 🔹 Integrated with **React Frontend** (on port `5173`)

---

## 📁 Project Structure

Server/
├── app/
│ ├── init.py
│ ├── models.py
│ ├── config.py
│ ├── routes/
│ │ ├── patients.py
│ │ ├── doctors.py
│ │ ├── appointments.py
│ │ ├── departments.py
│ │ └── medical_records.py
├── instance/
│ └── app.db
├── migrations/
├── run.py
├── requirements.txt
└── README.md


##  Getting Started

1. Clone the Repository

2. Set Up Environment
Make sure you have Python 3.8+ installed.
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Run Migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

5. Start the Server
python run.py
Server will run at:
➡️ http://localhost:5555

📬 API Endpoints
Resource	        Endpoint	        Methods
Patients	        /patients/	        GET, POST
Single Patient	   /patients/<id>	    GET, DELETE
Medical Records	    /records/	        GET, POST
Single Record	    /records/<id>	    GET, PATCH, DELETE
Appointments	   /appointments/	    GET, POST
Departments 	  /departments/	        GET, POST
Doctors	            /doctors/	        GET, POST

📌 Environment Variables
Create a .env file in your project root (if needed):

SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///hospital.db


📄 License
This project is licensed under the MIT License.

MIT License


🤝 Acknowledgements
Special thanks to the Moringa School curriculum and instructors for guidance and mentorship throughout the project.

💡 For frontend integration, ensure CORS is enabled and your React frontend runs on http://localhost:5173.











