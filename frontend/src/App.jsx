import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import PredictionForm from './pages/PredictionForm';
import History from './pages/History';
import DoctorDashboard from './pages/DoctorDashboard';

import ProtectedRoute from './components/ProtectedRoute';

function App() {
    return (
        <BrowserRouter>
            <Navbar />
            <Routes>
                <Route path="/" element={<Navigate to="/login" replace />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />

                {/* Protected Routes */}
                <Route element={<ProtectedRoute />}>
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/predict" element={<PredictionForm />} />
                    <Route path="/history" element={<History />} />
                    <Route path="/doctor" element={<DoctorDashboard />} />
                </Route>
            </Routes>
        </BrowserRouter>
    )
}
export default App;
