
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';

import Home from './pages/Home';
import Patients from './pages/Patients';
import Doctors from './pages/Doctors';
import Appointments from './pages/Appointments';
import Departments from './pages/Departments';
import Records from './pages/Records';

const App = () => {
  return (
    <Router>
      <div className="flex">
        <Navbar />
        <div className="flex-1 min-h-screen bg-gray-50">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/patients" element={<Patients />} />
            <Route path="/doctors" element={<Doctors />} />
            <Route path="/appointments" element={<Appointments />} />
            <Route path="/departments" element={<Departments />} />
            <Route path="/records" element={<Records />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;

