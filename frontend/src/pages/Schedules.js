import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Modal, Form, Alert } from 'react-bootstrap';
import Navbar from '../components/layout/Navbar';
import { api } from '../services/api';

const Schedules = () => {
  const [schedules, setSchedules] = useState([]);
  const [contents, setContents] = useState([]);
  const [agencies, setAgencies] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editingSchedule, setEditingSchedule] = useState(null);
  const [formData, setFormData] = useState({
    content_id: '',
    agency_id: '',
    start_time: '08:00',
    end_time: '18:00',
    days_of_week: [],
    priority: 1,
    is_active: true
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchSchedules();
    fetchContents();
    fetchAgencies();
  }, []);

  const fetchSchedules = async () => {
    try {
      const response = await api.get('/schedules');
      setSchedules(response.data);
    } catch (error) {
      setError('Erro ao carregar agendamentos');
    }
  };

  const fetchContents = async () => {
    try {
      const response = await api.get('/contents');
      setContents(response.data);
    } catch (error) {
      console.error('Erro ao carregar conteúdos');
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
      const scheduleData = {
        ...formData,
        days_of_week: formData.days_of_week.join(',')
      };

      if (editingSchedule) {
        await api.put(`/schedules/${editingSchedule.id}`, scheduleData);
        setSuccess('Agendamento atualizado com sucesso!');
      } else {
        await api.post('/schedules', scheduleData);
        setSuccess('Agendamento criado com sucesso!');
      }
      setShowModal(false);
      setEditingSchedule(null);
      resetForm();
      fetchSchedules();
    } catch (error) {
      setError('Erro ao salvar agendamento');
    }
  };

  const handleEdit = (schedule) => {
    setEditingSchedule(schedule);
    setFormData({
      content_id: schedule.content_id,
      agency_id: schedule.agency_id,
      start_time: schedule.start_time,
      end_time: schedule.end_time,
      days_of_week: schedule.days_of_week.split(','),
      priority: schedule.priority,
      is_active: schedule.is_active
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este agendamento?')) {
      try {
        await api.delete(`/schedules/${id}`);
        setSuccess('Agendamento excluído com sucesso!');
        fetchSchedules();
      } catch (error) {
        setError('Erro ao excluir agendamento');
      }
    }
  };

  const handleDayToggle = (day) => {
    setFormData(prev => ({
      ...prev,
      days_of_week: prev.days_of_week.includes(day)
        ? prev.days_of_week.filter(d => d !== day)
        : [...prev.days_of_week, day]
    }));
  };

  const resetForm = () => {
    setFormData({
      content_id: '',
      agency_id: '',
      start_time: '08:00',
      end_time: '18:00',
      days_of_week: [],
      priority: 1,
      is_active: true
    });
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingSchedule(null);
    resetForm();
  };

  const getContentTitle = (contentId) => {
    const content = contents.find(c => c.id === contentId);
    return content ? content.title : 'Conteúdo não encontrado';
  };

  const getAgencyName = (agencyId) => {
    const agency = agencies.find(a => a.id === agencyId);
    return agency ? agency.name : 'Agência não encontrada';
  };

  const getDaysOfWeekText = (daysString) => {
    const days = daysString.split(',');
    const dayNames = {
      '0': 'Dom',
      '1': 'Seg',
      '2': 'Ter',
      '3': 'Qua',
      '4': 'Qui',
      '5': 'Sex',
      '6': 'Sáb'
    };
    return days.map(day => dayNames[day]).join(', ');
  };

  return (
    <>
      <Navbar />
      <Container fluid className="mt-4">
        <Row>
          <Col>
            <div className="d-flex justify-content-between align-items-center mb-4">
              <h2>Gerenciar Agendamentos</h2>
              <Button
                variant="success"
                onClick={() => setShowModal(true)}
                style={{ backgroundColor: '#006633', borderColor: '#006633' }}
              >
                Novo Agendamento
              </Button>
            </div>

            {error && <Alert variant="danger">{error}</Alert>}
            {success && <Alert variant="success">{success}</Alert>}

            <Row>
              {schedules.map((schedule) => (
                <Col md={6} key={schedule.id} className="mb-4">
                  <Card>
                    <Card.Body>
                      <div className="d-flex justify-content-between align-items-start mb-3">
                        <div>
                          <Card.Title className="mb-1">
                            {getContentTitle(schedule.content_id)}
                          </Card.Title>
                          <small className="text-muted">
                            {getAgencyName(schedule.agency_id)}
                          </small>
                        </div>
                        <div className="text-end">
                          <span className={`badge ${schedule.is_active ? 'bg-success' : 'bg-secondary'}`}>
                            {schedule.is_active ? 'Ativo' : 'Inativo'}
                          </span>
                        </div>
                      </div>

                      <Card.Text>
                        <div className="mb-2">
                          <strong>Horário:</strong> {schedule.start_time} - {schedule.end_time}
                        </div>
                        <div className="mb-2">
                          <strong>Dias:</strong> {getDaysOfWeekText(schedule.days_of_week)}
                        </div>
                        <div className="mb-2">
                          <strong>Prioridade:</strong> {schedule.priority}
                        </div>
                      </Card.Text>

                      <div className="d-flex gap-2">
                        <Button
                          variant="outline-primary"
                          size="sm"
                          onClick={() => handleEdit(schedule)}
                        >
                          Editar
                        </Button>
                        <Button
                          variant="outline-danger"
                          size="sm"
                          onClick={() => handleDelete(schedule.id)}
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

        <Modal show={showModal} onHide={handleCloseModal} size="lg">
          <Modal.Header closeButton>
            <Modal.Title>
              {editingSchedule ? 'Editar Agendamento' : 'Novo Agendamento'}
            </Modal.Title>
          </Modal.Header>
          <Form onSubmit={handleSubmit}>
            <Modal.Body>
              <Form.Group className="mb-3">
                <Form.Label>Conteúdo</Form.Label>
                <Form.Select
                  value={formData.content_id}
                  onChange={(e) => setFormData({...formData, content_id: e.target.value})}
                  required
                >
                  <option value="">Selecione um conteúdo</option>
                  {contents.map(content => (
                    <option key={content.id} value={content.id}>
                      {content.title} ({content.type})
                    </option>
                  ))}
                </Form.Select>
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

              <Row>
                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Horário de Início</Form.Label>
                    <Form.Control
                      type="time"
                      value={formData.start_time}
                      onChange={(e) => setFormData({...formData, start_time: e.target.value})}
                      required
                    />
                  </Form.Group>
                </Col>
                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Horário de Fim</Form.Label>
                    <Form.Control
                      type="time"
                      value={formData.end_time}
                      onChange={(e) => setFormData({...formData, end_time: e.target.value})}
                      required
                    />
                  </Form.Group>
                </Col>
              </Row>

              <Form.Group className="mb-3">
                <Form.Label>Dias da Semana</Form.Label>
                <div className="d-flex flex-wrap gap-2">
                  {[
                    { key: '1', label: 'Seg' },
                    { key: '2', label: 'Ter' },
                    { key: '3', label: 'Qua' },
                    { key: '4', label: 'Qui' },
                    { key: '5', label: 'Sex' },
                    { key: '6', label: 'Sáb' },
                    { key: '0', label: 'Dom' }
                  ].map(day => (
                    <Form.Check
                      key={day.key}
                      type="checkbox"
                      label={day.label}
                      checked={formData.days_of_week.includes(day.key)}
                      onChange={() => handleDayToggle(day.key)}
                    />
                  ))}
                </div>
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Prioridade</Form.Label>
                <Form.Control
                  type="number"
                  min="1"
                  max="10"
                  value={formData.priority}
                  onChange={(e) => setFormData({...formData, priority: parseInt(e.target.value)})}
                />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Check
                  type="checkbox"
                  label="Agendamento ativo"
                  checked={formData.is_active}
                  onChange={(e) => setFormData({...formData, is_active: e.target.checked})}
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
                {editingSchedule ? 'Atualizar' : 'Criar'}
              </Button>
            </Modal.Footer>
          </Form>
        </Modal>
      </Container>
    </>
  );
};

export default Schedules;
