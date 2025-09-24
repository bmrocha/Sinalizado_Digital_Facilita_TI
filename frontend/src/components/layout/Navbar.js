import React from 'react';
import { Navbar as BootstrapNavbar, Nav, NavDropdown, Container } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <BootstrapNavbar bg="success" variant="dark" expand="lg" sticky="top">
      <Container fluid>
        <BootstrapNavbar.Brand as={Link} to="/dashboard" className="fw-bold">
          <i className="fas fa-tv me-2"></i>
          Sinalização Digital
        </BootstrapNavbar.Brand>

        <BootstrapNavbar.Toggle aria-controls="basic-navbar-nav" />

        <BootstrapNavbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/dashboard">
              <i className="fas fa-tachometer-alt me-1"></i>
              Dashboard
            </Nav.Link>

            <Nav.Link as={Link} to="/agencies">
              <i className="fas fa-building me-1"></i>
              Agências
            </Nav.Link>

            <Nav.Link as={Link} to="/contents">
              <i className="fas fa-file-alt me-1"></i>
              Conteúdos
            </Nav.Link>

            <Nav.Link as={Link} to="/schedules">
              <i className="fas fa-calendar-alt me-1"></i>
              Agendamentos
            </Nav.Link>

            <Nav.Link as={Link} to="/devices">
              <i className="fas fa-desktop me-1"></i>
              Dispositivos
            </Nav.Link>
          </Nav>

          <Nav>
            <NavDropdown
              title={
                <span>
                  <i className="fas fa-user me-1"></i>
                  {user?.full_name || user?.username}
                </span>
              }
              id="user-dropdown"
              align="end"
            >
              <NavDropdown.Item as={Link} to="/profile">
                <i className="fas fa-user-edit me-2"></i>
                Perfil
              </NavDropdown.Item>

              <NavDropdown.Item as={Link} to="/settings">
                <i className="fas fa-cog me-2"></i>
                Configurações
              </NavDropdown.Item>

              <NavDropdown.Divider />

              <NavDropdown.Item onClick={handleLogout}>
                <i className="fas fa-sign-out-alt me-2"></i>
                Sair
              </NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </BootstrapNavbar.Collapse>
      </Container>
    </BootstrapNavbar>
  );
};

export default Navbar;
