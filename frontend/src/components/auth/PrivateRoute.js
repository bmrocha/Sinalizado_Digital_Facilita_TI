import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { Spinner, Container } from 'react-bootstrap';
import { useAuth } from '../../context/AuthContext';

const PrivateRoute = ({ children }) => {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <Container className="d-flex justify-content-center align-items-center min-vh-100">
        <div className="text-center">
          <Spinner animation="border" variant="success" className="mb-3" />
          <p className="text-muted">Carregando...</p>
        </div>
      </Container>
    );
  }

  if (!user) {
    // Redirect to login page with return url
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
};

export default PrivateRoute;
