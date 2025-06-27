import { Routes, Route, Link } from 'react-router-dom';
import Appointments from './pages/Appointments';
import Doctors from './pages/Doctors';

function App() {
  return (
    <>
      <nav style={{ padding: '1rem', borderBottom: '1px solid #ccc' }}>
        <Link to="/appointments">Appointments</Link> |{" "}
        <Link to="/doctors">Doctors</Link>
      </nav>

      <Routes>
        <Route path="/appointments" element={<Appointments />} />
        <Route path="/doctors" element={<Doctors />} />
        <Route path="*" element={<h2>Welcome to Hospital System</h2>} />
      </Routes>
    </>
  );
}

export default App;

