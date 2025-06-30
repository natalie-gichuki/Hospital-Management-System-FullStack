# 🏥 Hospital Management System

A full-stack ⚙️ **Hospital Management System** built with a modern **React + Vite + Tailwind** frontend and a robust **Flask + SQLAlchemy** backend. The system streamlines core hospital operations like managing patients, doctors, appointments, records, and departments.

> 📍 Designed with responsiveness, modularity, and scalability in mind

---

## ⚡️ Tech Stack

<p align="left">
  <img src="https://img.shields.io/badge/Frontend-React-blue?style=for-the-badge&logo=react" />
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" />
</p>
<p align="left">
  <img src="https://img.shields.io/badge/Backend-Flask-black?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/ORM-SQLAlchemy-red?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/DB-SQLite-blue?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/Form-Formik-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Yup-Validation-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/API-REST_JSON-yellow?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Postman-Test-orange?style=for-the-badge&logo=postman" />
</p>

---

## ✨ Key Features

### 🖥️ Frontend
- 🧍 Patient Management (Add/View/Delete)
- 🧑‍⚕️ Doctor Profiles with Specializations
- 🗓️ Appointment Booking and Scheduling
- 🏬 Department Creation & Head Assignment
- 📋 Medical Records (View/Create/Update/Delete)
- 📱 Responsive Design for all devices
- 🌀 Infinite scroll tech stack badges (scroll above!)

### ⚙️ Backend
- ✅ Full CRUD API for all entities
- 🧬 Polymorphic Inpatient/Outpatient handling
- 🧠 Linked records and appointments for continuity
- 📦 Modular Blueprint route structure
- 🚀 Swagger-ready RESTful endpoints

---

## 🗂️ Project Structure

### 🔹 Frontend
``` bash
client/
├── public/
├── src/
│   ├── assets/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
```
### 🔸 Backend
``` bash 
server/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── config.py
│   └── routes/
├── instance/
├── migrations/
├── run.py
├── requirements.txt
```
# 🚀 Getting Started
## 🛠️ Backend
``` bash ```
- Copy

- git clone https://github.com/natalie-gichuki/Hospital-Management-System-FullStack.git
- cd Hospital-Management-System-FullStack/server

### Setup Python environment
- python3 -m venv venv
- source venv/bin/activate

### Install and migrate DB
- pip install -r requirements.txt
- flask db init
- flask db migrate -m "init"
- flask db upgrade

### Start server
- python run.py
>> 📍 Backend runs at: http://localhost:5555

## 🌐 Frontend
bash
- Copy
  
- cd ../client
- npm install

# Setup environment
- echo "VITE_API_BASE_URL=http://localhost:5555" > .env

# Run the client
- npm run dev
>> 📍 Frontend runs at: http://localhost:5173

## 🔗 API Endpoints
* Resource	Endpoint	Methods
* Patients	/patients/	GET, POST
* Patient Detail	/patients/<id>	GET, DELETE
* Records	/records/	GET, POST
* Record Detail	/records/<id>	GET, PATCH, DELETE
* Appointments	/appointments/	GET, POST
* Departments	/departments/	GET, POST
* Doctors	/doctors/	GET, POST

## 🎨 Styling Guidelines
- Tailwind CSS mobile-first design

- Clean layout, utility-first components

- Animations with Tailwind and Framer Motion

- Accessibility-first: readable fonts, semantic tags

## 💡 Best Practices
✅ Component-based design

✅ RESTful routes with meaningful responses

✅ Formik + Yup validation

✅ Blueprints for backend modularity

✅ CORS-safe frontend/backend interaction

✅ Version-controlled DB migrations

## 🚧 Future Enhancements
🔐 Auth system (Role-based Access Control)

📊 Analytics Dashboard (Recharts/D3)

🌙 Dark Mode Toggle

🌍 Internationalization (i18n)

🔄 Real-time Appointments (WebSockets)

✅ Full Unit and Integration Testing

## 🤝 Contributing
```bash```
- Copy
  
#### Step-by-step
1. Fork the repo
2. Create feature branch: git checkout -b feature/AmazingFeature
3. Commit: git commit -m "Add AmazingFeature"
4. Push: git push origin feature/AmazingFeature
5. Submit Pull Request
### 👥 Authors
## 👩‍💻 Gichuki Natalie

## 👨‍💻 Kipsang Jesse

## 👨‍💻 Kihikah Kariuki

# Special thanks to Moringa School 🎓

### 📄 License
MIT License

### 🔗 Project Link
👉 GitHub Repository
