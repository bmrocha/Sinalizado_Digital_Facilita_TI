import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Modal, Form, Alert } from 'react-bootstrap';
import Navbar from '../components/layout/Navbar';
import { api } from '../services/api';

const Agencies = () => {
  const [agencies, setAgencies] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editingAgency, setEditingAgency] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    ip_address: '',
    orientation: 'horizontal',
    hibernation_enabled: true,
    hibernation_start: '18:00',
    hibernation_end: '08:00'
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchAgencies();
  }, []);

  const fetchAgencies = async () => {
    try {
      const response = await api.get('/agencies');
      setAgencies(response.data);
    } catch (error) {
      setError('Erro ao carregar agências');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingAgency) {
        await api.put(`/agencies/${editingAgency.id}`, formData);
        setSuccess('Agência atualizada com sucesso!');
      } else {
        await api.post('/agencies', formData);
        setSuccess('Agência criada com sucesso!');
      }
      setShowModal(false);
      setEditingAgency(null);
      resetForm();
      fetchAgencies();
    } catch (error) {
      setError('Erro ao salvar agência');
    }
  };

  const handleEdit = (agency) => {
    setEditingAgency(agency);
    setFormData({
      name: agency.name,
      ip_address: agency.ip_address,
      orientation: agency.orientation,
      hibernation_enabled: agency.hibernation_enabled,
      hibernation_start: agency.hibernation_start,
      hibernation_end: agency.hibernation_end
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir esta agência?')) {
      try {
        await api.delete(`/agencies/${id}`);
        setSuccess('Agência excluída com sucesso!');
        fetchAgencies();
      } catch (error) {
        setError('Erro ao excluir agência');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      ip_address: '',
      orientation: 'horizontal',
      hibernation_enabled: true,
      hibernation_start: '18:00',
      hibernation_end: '08:00'
    });
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingAgency(null);
    resetForm();
  };

  return (
    <>
      <Navbar />
      <Container fluid className="mt-4">
        <Row>
          <Col>
            <div className="d-flex justify-content-between align-items-center mb-4">
              <h2>Gerenciar Agências</h2>
              <Button
                variant="success"
                onClick={() => setShowModal(true)}
                style={{ backgroundColor: '#006633', borderColor: '#006633' }}
              >
                Nova Agência
              </Button>
            </div>

            {error && <Alert variant="danger">{error}</Alert>}
            {success && <Alert variant="success">{success}</Alert>}

            <Row>
              {agencies.map((agency) => (
                <Col md={4} key={agency.id} className="mb-4">
                  <Card>
                    <Card.Body>
                      <Card.Title>{agency.name}</Card.Title>
                      <Card.Text>
                        <strong>IP:</strong> {agency.ip_address}<br/>
                        <strong>Orientação:</strong> {agency.orientation === 'horizontal' ? 'Horizontal' : 'Vertical'}<br/>
                        <strong>Hibernação:</strong> {agency.hibernation_enabled ? 'Ativada' : 'Desativada'}
                      </Card.Text>
                      <div className="d-flex gap-2">
                        <Button
                          variant="outline-primary"
                          size="sm"
                          onClick={() => handleEdit(agency)}
                        >
                          Editar
                        </Button>
                        <Button
                          variant="outline-danger"
                          size="sm"
                          onClick={() => handleDelete(agency.id)}
                        >
                          Excluir
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
              {editingAgency ? 'Editar Agência' : 'Nova Agência'}
            </Modal.Title>
          </Modal.Header>
          <Form onSubmit={handleSubmit}>
            <Modal.Body>
              <Form.Group className="mb-3">
                <Form.Label>Nome da Agência</Form.Label>
                <Form.Control
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  required
                />
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
                <Form.Label>Orientação da Tela</Form.Label>
                <Form.Select
                  value={formData.orientation}
                  onChange={(e) => setFormData({...formData, orientation: e.target.value})}
                >
                  <option value="horizontal">Horizontal</option>
                  <option value="vertical">Vertical</option>
                </Form.Select>
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Check
                  type="checkbox"
                  label="Hibernação automática"
                  checked={formData.hibernation_enabled}
                  onChange={(e) => setFormData({...formData, hibernation_enabled: e.target.checked})}
                />
              </Form.Group>

              {formData.hibernation_enabled && (
                <>
                  <Form.Group className="mb-3">
                    <Form.Label>Início da Hibernação</Form.Label>
                    <Form.Control
                      type="time"
                      value={formData.hibernation_start}
                      onChange={(e) => setFormData({...formData, hibernation_start: e.target.value})}
                    />
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>Fim da Hibernação</Form.Label>
                    <Form.Control
                      type="time"
                      value={formData.hibernation_end}
                      onChange={(e) => setFormData({...formData, hibernation_end: e.target.value})}
                    />
                  </Form.Group>
                </>
              )}
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
                {editingAgency ? 'Atualizar' : 'Criar'}
              </Button>
            </Modal.Footer>
          </Form>
        </Modal>
      </Container>
    </>
  );
};

export default Agencies;
