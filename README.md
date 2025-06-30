### 🏥 HOSPITAL MANAGEMENT SYSTEM
A full-stack Hospital Management System with a React + Vite + Tailwind CSS frontend and a Flask + SQLAlchemy REST API backend. Built to streamline patient, doctor, appointment, and medical record management in a hospital environment.

## 🔧 Technologies Used
Layer                                | Tools Used
-------------------------------------|----------------------------------------------------
Frontend	                         |React, Vite, Tailwind CSS, React Router, Formik + Yup
Backend	                             |Python, Flask, Flask-RESTful, SQLAlchemy, Flask-Migrate
Database	                         |SQLite (via SQLAlchemy)
API Format	                         |JSON (via RESTful routes)
Other	                             |Flask-CORS, Postman

## ✨ Features
✅ Frontend Features
Patient Management: Add, view, and delete patient records

Doctor Management: Manage doctor profiles and specializations

Appointments: Book and view appointments

Departments: Create and organize hospital departments

Medical Records: View, create, update, and delete patient history

Responsive Design: Fully responsive across all devices

## 🧠 Backend Features
Full CRUD for Patients, Doctors, Appointments, Records, and Departments

Inpatient and Outpatient support via inheritance

Doctor-department assignments, including Head Doctor

Linked appointments and records for continuity

Modular structure using Flask Blueprints and RESTful Resources

## 🗂 Project Structure
📁 Frontend - client/

client/
├── public/
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── AppointmentForm.jsx
│   │   ├── DepartmentForm.jsx
│   │   ├── DoctorCard.jsx
│   │   ├── Navbar.jsx
│   │   ├── PatientForm.jsx
│   │   └── RecordTable.jsx
│   ├── pages/
│   │   ├── Appointments.jsx
│   │   ├── Departments.jsx
│   │   ├── Doctors.jsx
│   │   ├── Home.jsx
│   │   ├── Patients.jsx
│   │   └── Records.jsx
│   ├── services/
│   │   ├── AppointmentService.js
│   │   ├── DepartmentService.js
│   │   ├── DoctorService.js
│   │   ├── PatientService.js
│   │   ├── RecordService.js
│   │   └── api.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css

📁 Backend - server/

server/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── config.py
│   └── routes/
│       ├── patients.py
│       ├── doctors.py
│       ├── appointments.py
│       ├── departments.py
│       └── medical_records.py
├── instance/
│   └── app.db
├── migrations/
├── run.py
├── requirements.txt

## 🚀 Getting Started
🛠 Backend Setup

# Clone the repo and navigate to backend
git clone 
cd hospital-management-system/server

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize DB
flask db init
flask db migrate -m "Initial"
flask db upgrade

# Run the server
python run.py
Backend runs at: http://localhost:5555

🌐 Frontend Setup

# Navigate to frontend folder
cd ../client

# Install dependencies
npm install

# Create .env file
echo "VITE_API_BASE_URL=http://localhost:5555" > .env

# Start frontend server
npm run dev
Frontend runs at: http://localhost:5173

🔗 API Endpoints
Resource	                Endpoint	          Methods
Patients	                /patients/	         GET, POST
Single Patient	            /patients/<id>	     GET, DELETE
Records	                    /records/	         GET, POST
Single Record	            /records/<id>	     GET, PATCH, DELETE
Appointments	            /appointments/	     GET, POST
Departments	                /departments/	     GET, POST
Doctors	                    /doctors/	         GET, POST

## 🎨 Styling Guidelines
Tailwind CSS with mobile-first responsive design

Reusable components and utility classes

Clean, minimal layout with focus on accessibility

Transitions and animations for better UX

Custom theme in tailwind.config.js

## 💡 Best Practices
Component-based architecture in React

Separation of logic: services, components, views

Form validation using Formik + Yup

Graceful error handling and feedback

RESTful API design with clear structure

Version-controlled database migrations

Secure CORS setup for frontend-backend communication

## 📈 Future Improvements
🔐 User Authentication and Role-based Access

📊 Charts and analytics dashboard

🕒 Real-time notifications with WebSockets

🌙 Dark mode toggle

🌍 Internationalization support

✅ Unit and integration tests

## 🤝 Contributing
Fork the repo

Create your branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

🧑‍💻 Authors
This project was proudly built by:

*** Gichuki Natalie ***
*** Kipsang Jesse ***
*** Kihikah Kariuki ***

Special thanks to Moringa School for their mentorship and guidance.

📄 License
Distributed under the MIT License.

## Project Link ```https://github.com/natalie-gichuki/Hospital-Management-System-FullStack.git```