import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Container } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

// Components
import Login from './components/auth/Login';
import Dashboard from './components/dashboard/Dashboard';
import Navbar from './components/layout/Navbar';
import PrivateRoute from './components/auth/PrivateRoute';

// Pages
import Home from './pages/Home';
import Agencies from './pages/Agencies';
import Contents from './pages/Contents';
import Schedules from './pages/Schedules';
import Devices from './pages/Devices';

// Context
import { AuthProvider } from './context/AuthContext';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={
              <PrivateRoute>
                <Navbar />
                <Container fluid className="main-container">
                  <Routes>
                    <Route path="/dashboard" element={<Home />} />
                    <Route path="/agencies" element={<Agencies />} />
                    <Route path="/contents" element={<Contents />} />
                    <Route path="/schedules" element={<Schedules />} />
                    <Route path="/devices" element={<Devices />} />
                    <Route path="/" element={<Navigate to="/dashboard" replace />} />
                  </Routes>
                </Container>
              </PrivateRoute>
            } />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
