import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Spinner, Alert } from 'react-bootstrap';
import axios from 'axios';

const Dashboard = () => {
  const [stats, setStats] = useState({
    agencies: 0,
    contents: 0,
    schedules: 0,
    devices: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const [agenciesRes, contentsRes, schedulesRes, devicesRes] = await Promise.all([
        axios.get('/agencies'),
        axios.get('/contents'),
        axios.get('/schedules'),
        axios.get('/devices')
      ]);

      setStats({
        agencies: agenciesRes.data.length,
        contents: contentsRes.data.length,
        schedules: schedulesRes.data.length,
        devices: devicesRes.data.filter(d => d.is_online).length
      });
    } catch (err) {
      setError('Erro ao carregar estatísticas');
      console.error('Error fetching stats:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-5">
        <Spinner animation="border" variant="success" />
        <p className="mt-2 text-muted">Carregando dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="danger">
        {error}
      </Alert>
    );
  }

  const statCards = [
    {
      title: 'Agências',
      value: stats.agencies,
      icon: 'fas fa-building',
      color: 'success',
      bgColor: 'rgba(0, 102, 51, 0.1)',
      link: '/agencies'
    },
    {
      title: 'Conteúdos',
      value: stats.contents,
      icon: 'fas fa-file-alt',
      color: 'info',
      bgColor: 'rgba(23, 162, 184, 0.1)',
      link: '/contents'
    },
    {
      title: 'Agendamentos',
      value: stats.schedules,
      icon: 'fas fa-calendar-alt',
      color: 'warning',
      bgColor: 'rgba(255, 193, 7, 0.1)',
      link: '/schedules'
    },
    {
      title: 'Dispositivos Online',
      value: stats.devices,
      icon: 'fas fa-desktop',
      color: 'primary',
      bgColor: 'rgba(13, 110, 253, 0.1)',
      link: '/devices'
    }
  ];

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1 className="h3 mb-0 text-success">
          <i className="fas fa-tachometer-alt me-2"></i>
          Dashboard
        </h1>
        <small className="text-muted">
          Bem-vindo ao Sistema de Sinalização Digital
        </small>
      </div>

      <Row>
        {statCards.map((card, index) => (
          <Col key={index} lg={3} md={6} sm={12} className="mb-4">
            <Card
              className="dashboard-card h-100"
              style={{ cursor: 'pointer' }}
              onClick={() => window.location.href = card.link}
            >
              <Card.Body className="text-center">
                <div
                  className="dashboard-card-icon mx-auto mb-3"
                  style={{
                    backgroundColor: card.bgColor,
                    color: `var(--sicoob-${card.color})`
                  }}
                >
                  <i className={card.icon} style={{ fontSize: '1.5rem' }}></i>
                </div>
                <h3 className="h5 text-dark mb-1">{card.title}</h3>
                <h2 className="h3 text-success fw-bold mb-0">{card.value}</h2>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      <Row className="mt-4">
        <Col lg={8}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">
                <i className="fas fa-chart-line me-2"></i>
                Atividade Recente
              </h5>
            </Card.Header>
            <Card.Body>
              <div className="text-center py-4 text-muted">
                <i className="fas fa-clock fa-2x mb-3"></i>
                <p>Histórico de atividades será exibido aqui</p>
              </div>
            </Card.Body>
          </Card>
        </Col>

        <Col lg={4}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">
                <i className="fas fa-info-circle me-2"></i>
                Status do Sistema
              </h5>
            </Card.Header>
            <Card.Body>
              <div className="d-flex justify-content-between align-items-center mb-2">
                <span>API Status</span>
                <span className="badge bg-success">Online</span>
              </div>
              <div className="d-flex justify-content-between align-items-center mb-2">
                <span>Database</span>
                <span className="badge bg-success">Conectado</span>
              </div>
              <div className="d-flex justify-content-between align-items-center">
                <span>Dispositivos</span>
                <span className="badge bg-warning">{stats.devices} Online</span>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
