import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Modal, Form, Alert, Badge } from 'react-bootstrap';
import Navbar from '../components/layout/Navbar';
import { api } from '../services/api';

const Devices = () => {
  const [devices, setDevices] = useState([]);
  const [agencies, setAgencies] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editingDevice, setEditingDevice] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    agency_id: '',
    ip_address: '',
    mac_address: '',
    status: 'offline',
    last_seen: null,
    version: '1.0.0'
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchDevices();
    fetchAgencies();
  }, []);

  const fetchDevices = async () => {
    try {
      const response = await api.get('/devices');
      setDevices(response.data);
    } catch (error) {
      setError('Erro ao carregar dispositivos');
    }
  };

  const fetchAgencies = async () => {
    try {
      const response = await api.get('/agencies');
      setAgencies(response.data);
    } catch (error) {
      console.error('Erro ao carregar agências');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingDevice) {
        await api.put(`/devices/${editingDevice.id}`, formData);
        setSuccess('Dispositivo atualizado com sucesso!');
      } else {
        await api.post('/devices', formData);
        setSuccess('Dispositivo criado com sucesso!');
      }
      setShowModal(false);
      setEditingDevice(null);
      resetForm();
      fetchDevices();
    } catch (error) {
      setError('Erro ao salvar dispositivo');
    }
  };

  const handleEdit = (device) => {
    setEditingDevice(device);
    setFormData({
      name: device.name,
      agency_id: device.agency_id,
      ip_address: device.ip_address,
      mac_address: device.mac_address,
      status: device.status,
      last_seen: device.last_seen,
      version: device.version
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este dispositivo?')) {
      try {
        await api.delete(`/devices/${id}`);
        setSuccess('Dispositivo excluído com sucesso!');
        fetchDevices();
      } catch (error) {
        setError('Erro ao excluir dispositivo');
      }
    }
  };

  const handleStatusUpdate = async (deviceId, newStatus) => {
    try {
      await api.put(`/devices/${deviceId}/status`, { status: newStatus });
      setSuccess(`Status do dispositivo atualizado para ${newStatus}`);
      fetchDevices();
    } catch (error) {
      setError('Erro ao atualizar status do dispositivo');
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      agency_id: '',
      ip_address: '',
      mac_address: '',
      status: 'offline',
      last_seen: null,
      version: '1.0.0'
    });
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingDevice(null);
    resetForm();
  };

  const getAgencyName = (agencyId) => {
    const agency = agencies.find(a => a.id === agencyId);
    return agency ? agency.name : 'Agência não encontrada';
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      online: { variant: 'success', text: 'Online' },
      offline: { variant: 'secondary', text: 'Offline' },
      error: { variant: 'danger', text: 'Erro' },
      maintenance: { variant: 'warning', text: 'Manutenção' }
    };

    const config = statusConfig[status] || statusConfig.offline;
    return (
      <Badge bg={config.variant}>
        {config.text}
      </Badge>
    );
  };

  const formatLastSeen = (lastSeen) => {
    if (!lastSeen) return 'Nunca';
    const date = new Date(lastSeen);
    return date.toLocaleString('pt-BR');
  };

  return (
    <>
      <Navbar />
      <Container fluid className="mt-4">
        <Row>
          <Col>
            <div className="d-flex justify-content-between align-items-center mb-4">
              <h2>Gerenciar Dispositivos</h2>
              <Button
                variant="success"
                onClick={() => setShowModal(true)}
                style={{ backgroundColor: '#006633', borderColor: '#006633' }}
              >
                Novo Dispositivo
              </Button>
            </div>

            {error && <Alert variant="danger">{error}</Alert>}
            {success && <Alert variant="success">{success}</Alert>}

            <Row>
              {devices.map((device) => (
                <Col md={4} key={device.id} className="mb-4">
                  <Card>
                    <Card.Body>
                      <div className="d-flex justify-content-between align-items-start mb-3">
                        <div>
                          <Card.Title className="mb-1">{device.name}</Card.Title>
                          <small className="text-muted">
                            {getAgencyName(device.agency_id)}
                          </small>
                        </div>
                        {getStatusBadge(device.status)}
                      </div>

                      <Card.Text>
                        <div className="mb-2">
                          <strong>IP:</strong> {device.ip_address}
                        </div>
                        {device.mac_address && (
                          <div className="mb-2">
                            <strong>MAC:</strong> {device.mac_address}
                          </div>
                        )}
                        <div className="mb-2">
                          <strong>Versão:</strong> {device.version}
                        </div>
                        <div className="mb-2">
                          <strong>Última conexão:</strong> {formatLastSeen(device.last_seen)}
                        </div>
                      </Card.Text>

                      <div className="d-flex gap-2">
                        <Button
                          variant="outline-primary"
                          size="sm"
                          onClick={() => handleEdit(device)}
                        >
                          Editar
                        </Button>
                        <Button
                          variant="outline-danger"
                          size="sm"
                          onClick={() => handleDelete(device.id)}
                        >
                          Excluir
                        </Button>
                      </div>

                      <div className="d-flex gap-1 mt-2">
                        <Button
                          variant="outline-success"
                          size="sm"
                          onClick={() => handleStatusUpdate(device.id, 'online')}
                          disabled={device.status === 'online'}
                        >
                          Online
                        </Button>
                        <Button
                          variant="outline-secondary"
                          size="sm"
                          onClick={() => handleStatusUpdate(device.id, 'offline')}
                          disabled={device.status === 'offline'}
                        >
                          Offline
                        </Button>
                        <Button
                          variant="outline-warning"
                          size="sm"
                          onClick={() => handleStatusUpdate(device.id, 'maintenance')}
                          disabled={device.status === 'maintenance'}
                        >
                          Manutenção
                        </Button>
                      </div>
                    </Card.Body>
                  </Card>
                </Col>
              ))}
            </Row>
          </Col>
        </Row>

        <Modal show={showModal} onHide={handleCloseModal}>
          <Modal.Header closeButton>
            <Modal.Title>
              {editingDevice ? 'Editar Dispositivo' : 'Novo Dispositivo'}
            </Modal.Title>
          </Modal.Header>
          <Form onSubmit={handleSubmit}>
            <Modal.Body>
              <Form.Group className="mb-3">
                <Form.Label>Nome do Dispositivo</Form.Label>
                <Form.Control
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  placeholder="Raspberry Pi Agência Centro"
                  required
                />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Agência</Form.Label>
                <Form.Select
                  value={formData.agency_id}
                  onChange={(e) => setFormData({...formData, agency_id: e.target.value})}
                  required
                >
                  <option value="">Selecione uma agência</option>
                  {agencies.map(agency => (
                    <option key={agency.id} value={agency.id}>
                      {agency.name} - {agency.ip_address}
                    </option>
                  ))}
                </Form.Select>
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Endereço IP</Form.Label>
                <Form.Control
                  type="text"
                  value={formData.ip_address}
                  onChange={(e) => setFormData({...formData, ip_address: e.target.value})}
                  placeholder="192.168.1.100"
                  required
                />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Endereço MAC (opcional)</Form.Label>
                <Form.Control
                  type="text"
                  value={formData.mac_address}
                  onChange={(e) => setFormData({...formData, mac_address: e.target.value})}
                  placeholder="AA:BB:CC:DD:EE:FF"
                />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Status Inicial</Form.Label>
                <Form.Select
                  value={formData.status}
                  onChange={(e) => setFormData({...formData, status: e.target.value})}
                >
                  <option value="offline">Offline</option>
                  <option value="online">Online</option>
                  <option value="maintenance">Manutenção</option>
                </Form.Select>
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Versão do Software</Form.Label>
                <Form.Control
                  type="text"
                  value={formData.version}
                  onChange={(e) => setFormData({...formData, version: e.target.value})}
                  placeholder="1.0.0"
                />
              </Form.Group>
            </Modal.Body>
            <Modal.Footer>
              <Button variant="secondary" onClick={handleCloseModal}>
                Cancelar
              </Button>
              <Button
                variant="success"
                type="submit"
                style={{ backgroundColor: '#006633', borderColor: '#006633' }}
              >
                {editingDevice ? 'Atualizar' : 'Criar'}
              </Button>
            </Modal.Footer>
          </Form>
        </Modal>
      </Container>
    </>
  );
};

export default Devices;
