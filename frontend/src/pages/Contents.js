import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Modal, Form, Alert } from 'react-bootstrap';
import Navbar from '../components/layout/Navbar';
import { api } from '../services/api';

const Contents = () => {
  const [contents, setContents] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editingContent, setEditingContent] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    type: 'link',
    url: '',
    description: '',
    duration: 30
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    fetchContents();
  }, []);

  const fetchContents = async () => {
    try {
      const response = await api.get('/contents');
      setContents(response.data);
    } catch (error) {
      setError('Erro ao carregar conteúdos');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingContent) {
        await api.put(`/contents/${editingContent.id}`, formData);
        setSuccess('Conteúdo atualizado com sucesso!');
      } else {
        await api.post('/contents', formData);
        setSuccess('Conteúdo criado com sucesso!');
      }
      setShowModal(false);
      setEditingContent(null);
      resetForm();
      fetchContents();
    } catch (error) {
      setError('Erro ao salvar conteúdo');
    }
  };

  const handleEdit = (content) => {
    setEditingContent(content);
    setFormData({
      title: content.title,
      type: content.type,
      url: content.url,
      description: content.description,
      duration: content.duration
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este conteúdo?')) {
      try {
        await api.delete(`/contents/${id}`);
        setSuccess('Conteúdo excluído com sucesso!');
        fetchContents();
      } catch (error) {
        setError('Erro ao excluir conteúdo');
      }
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    try {
      const formDataUpload = new FormData();
      formDataUpload.append('file', file);

      const response = await api.post('/contents/upload', formDataUpload, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setFormData({
        ...formData,
        url: response.data.url,
        type: file.type.startsWith('video/') ? 'video' : 'image'
      });

      setSuccess('Arquivo enviado com sucesso!');
    } catch (error) {
      setError('Erro ao fazer upload do arquivo');
    } finally {
      setUploading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      title: '',
      type: 'link',
      url: '',
      description: '',
      duration: 30
    });
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingContent(null);
    resetForm();
  };

  const getContentIcon = (type) => {
    switch (type) {
      case 'link': return '🔗';
      case 'image': return '🖼️';
      case 'video': return '🎥';
      default: return '📄';
    }
  };

  return (
    <>
      <Navbar />
      <Container fluid className="mt-4">
        <Row>
          <Col>
            <div className="d-flex justify-content-between align-items-center mb-4">
              <h2>Gerenciar Conteúdos</h2>
              <Button
                variant="success"
                onClick={() => setShowModal(true)}
                style={{ backgroundColor: '#006633', borderColor: '#006633' }}
              >
                Novo Conteúdo
              </Button>
            </div>

            {error && <Alert variant="danger">{error}</Alert>}
            {success && <Alert variant="success">{success}</Alert>}

            <Row>
              {contents.map((content) => (
                <Col md={4} key={content.id} className="mb-4">
                  <Card>
                    <Card.Body>
                      <div className="d-flex align-items-center mb-3">
                        <span className="me-2" style={{ fontSize: '1.5rem' }}>
                          {getContentIcon(content.type)}
                        </span>
                        <div>
                          <Card.Title className="mb-1">{content.title}</Card.Title>
                          <small className="text-muted">
                            {content.type === 'link' ? 'Link' : content.type === 'image' ? 'Imagem' : 'Vídeo'}
                          </small>
                        </div>
                      </div>

                      <Card.Text>
                        {content.description && (
                          <div className="mb-2">
                            <strong>Descrição:</strong> {content.description}
                          </div>
                        )}
                        <div className="mb-2">
                          <strong>Duração:</strong> {content.duration}s
                        </div>
                        {content.url && (
                          <div className="mb-2">
                            <strong>URL:</strong>
                            <div className="text-truncate" style={{ maxWidth: '200px' }}>
                              {content.url}
                            </div>
                          </div>
                        )}
                      </Card.Text>

                      <div className="d-flex gap-2">
                        <Button
                          variant="outline-primary"
                          size="sm"
                          onClick={() => handleEdit(content)}
                        >
                          Editar
                        </Button>
                        <Button
                          variant="outline-danger"
                          size="sm"
                          onClick={() => handleDelete(content.id)}
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
              {editingContent ? 'Editar Conteúdo' : 'Novo Conteúdo'}
            </Modal.Title>
          </Modal.Header>
          <Form onSubmit={handleSubmit}>
            <Modal.Body>
              <Form.Group className="mb-3">
                <Form.Label>Título</Form.Label>
                <Form.Control
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  required
                />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Tipo de Conteúdo</Form.Label>
                <Form.Select
                  value={formData.type}
                  onChange={(e) => setFormData({...formData, type: e.target.value})}
                >
                  <option value="link">Link/URL</option>
                  <option value="image">Imagem</option>
                  <option value="video">Vídeo</option>
                </Form.Select>
              </Form.Group>

              {formData.type !== 'link' && (
                <Form.Group className="mb-3">
                  <Form.Label>Arquivo</Form.Label>
                  <Form.Control
                    type="file"
                    accept={formData.type === 'image' ? 'image/*' : 'video/*'}
                    onChange={handleFileUpload}
                    disabled={uploading}
                  />
                  {uploading && <small className="text-muted">Enviando arquivo...</small>}
                </Form.Group>
              )}

              <Form.Group className="mb-3">
                <Form.Label>URL/Link</Form.Label>
                <Form.Control
                  type="url"
                  value={formData.url}
                  onChange={(e) => setFormData({...formData, url: e.target.value})}
                  placeholder={formData.type === 'link' ? 'https://exemplo.com' : 'Arquivo será enviado automaticamente'}
                  required
                />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Descrição (opcional)</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={3}
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                />
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Duração (segundos)</Form.Label>
                <Form.Control
                  type="number"
                  min="5"
                  max="3600"
                  value={formData.duration}
                  onChange={(e) => setFormData({...formData, duration: parseInt(e.target.value)})}
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
                {editingContent ? 'Atualizar' : 'Criar'}
              </Button>
            </Modal.Footer>
          </Form>
        </Modal>
      </Container>
    </>
  );
};

export default Contents;
