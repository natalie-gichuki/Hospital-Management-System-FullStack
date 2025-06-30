### Hospital Management System - Frontend
A modern frontend for a Hospital Management System built with React, Vite, and Tailwind CSS.

Features
1. Patient Management: Create, view, and delete patient records
2. Doctor Management: Manage doctor profiles and specialties
3. Appointment Scheduling: Book and track patient appointments
4. Department Management: Organize hospital departments and staff
5. Medical Records: View and manage patient medical history
6. Responsive Design: Fully responsive interface for all devices

Project Structure

Client/
├── public/
│   └── vite.svg
├── src/
│   ├── assets/
│   │   └── react.svg
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
│   ├── index.css
│   └── main.jsx
├── .gitignore
├── index.html
├── package.json
├── postcss.config.js
├── README.md
├── tailwind.config.js
└── vite.config.js

### Technologies Used
1. React 18: JavaScript library for building user interfaces
2. Vite: Next-generation frontend tooling
3. Tailwind CSS: Utility-first CSS framework
4. React Router: Client-side routing
5. Formik & Yup: Form handling and validation
6. Fetch to link client and server


## Clone the repository:
git clone https://github.com/natalie-gichuki/Hospital-Management-System-FullStack.git
cd hospital-management-frontend


## Install dependencies:
npm install

## Configure environment variables:
Create a .env file in the root directory:

VITE_API_BASE_URL=http://localhost:5555

## Run the development server:

npm run dev

## Open your browser and visit:
http://localhost:5173
Available Scripts
npm run dev: Start development server


## API Integration
The frontend connects to a backend API with the following endpoints:

1. Appointments: /appointments
2. Departments: /departments
3. Doctors: /doctors
4. Patients: /patients
5. Records: /records

## Styling Approach
The application uses Tailwind CSS for styling with the following conventions:

Responsive design with mobile-first approach

Consistent spacing using Tailwind's spacing scale

Color palette defined in tailwind.config.js

Custom animations and transitions where needed

## Best Practices
1. Component-based architecture
2. Proper separation of concerns
3. Error boundaries for graceful error handling
4. Form validation with Yup
5. Proper state management
6. Responsive design principles
7. Accessibility considerations

## Future Improvements
1. Add user authentication
2. Implement role-based access control
3. Add charts for statistics and analytics
4. Implement real-time updates with WebSockets
5. Add dark mode support
6. Implement internationalization
7. Add unit and integration tests

## Contributing
Contributions are welcome! Please follow these steps:

Fork the project

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

License
Distributed under the MIT License. See LICENSE for more information.

Project was built by 
*** Jesse Kipsang ***
*** Natalie Gichuki ***
*** Kihikah Kariuki ***

Project Link: https://github.com/natalie-gichuki/Hospital-Management-System-FullStack.git
