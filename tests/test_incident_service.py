import pytest
from unittest.mock import MagicMock
from app.services.incident_service import IncidentService

# Fixture yang menyediakan instance IncidentService beserta mock dependency
@pytest.fixture
def incident_service():
   # Mock repository dan classifier agar tidak tergantung pada DB atau model nyata
   mock_repo = MagicMock()
   mock_classifier = MagicMock()
   
   # Simulasi hasil prediksi kategori incident: DATABASE
   mock_classifier.predict.return_value = "DATABASE"
   
   # Kembalikan service dengan dependency palsu untuk pengujian
   return IncidentService(repository=mock_repo, classifier=mock_classifier)

# Test: kondisi server down harus menghasilkan prioritas HIGH
def test_priority_high_when_server_down(incident_service):
   # Memanggil pembuatan incident dengan masalah kritis
   incident_service.create_incident(
      title="Server down",
      description="Production is not accessible",
      reported_by="user@example.com"
   )

   # Ambil objek incident yang disimpan ke repository untuk verifikasi
   args, _ = incident_service.repository.save.call_args
   saved_incident = args[0]
   
   # Prioritas harus tinggi karena layanan utama tidak tersedia
   assert saved_incident.priority == "HIGH"

# Test: error login harus diberi prioritas MEDIUM
def test_priority_medium_when_login_error(incident_service):
   # Membuat incident dengan masalah login yang tidak sepenuhnya fatal
   incident_service.create_incident(
      title="Login Issue",
      description="I got an error when logging in",
      reported_by="user@example.com"
   )
   
   # Ambil data incident yang baru saja disimpan
   args, _ = incident_service.repository.save.call_args
   saved_incident = args[0]
   
   # Validasi prioritas medium
   assert saved_incident.priority == "MEDIUM"

# Test: pertanyaan umum atau kebutuhan non-technical harus memiliki prioritas LOW
def test_priority_low_for_general_questions(incident_service):
   # Membuat incident untuk pertanyaan umum terkait perangkat
   incident_service.create_incident(
      title="Need new mouse",
      description="My mouse is broken",
      reported_by="user@example.com"
   )
   
   # Ambil incident yang dikirim ke repository
   args, _ = incident_service.repository.save.call_args
   saved_incident = args[0]
   
   # Prioritas harus rendah karena bukan masalah sistem
   assert saved_incident.priority == "LOW"

# Test: proses pembuatan incident berhasil dan mengembalikan data yang disimpan
def test_incident_creation_success(incident_service):
   # Simulasi repo.save berhasil dan mengembalikan incident dengan id dan status OPEN
   mock_saved_incident = MagicMock(id=1, status="OPEN")
   incident_service.repository.save.return_value = mock_saved_incident

   # Panggil method membuat incident
   result = incident_service.create_incident(
      title="System Issue", 
      description="Cannot process payment", 
      reported_by="user@test.com"
   )

   # Verifikasi output utama dari pembuatan incident
   assert result.id == 1
   assert result.status == "OPEN"
   incident_service.repository.save.assert_called_once()

# Test: saat data incident tidak ditemukan, service harus mengembalikan None
def test_incident_not_found(incident_service):
   # Simulasi repository tidak menemukan data sesuai id yang diminta
   incident_service.repository.get_by_id.return_value = None

   # Panggil query incident berdasarkan id
   result = incident_service.get_incident_by_id(9999)

   # Harus dikembalikan None apabila incident tidak ada
   assert result is None

# Test: service harus berinteraksi dengan repository melalui method save() saat create_incident dipanggil
def test_repository_service_interaction(incident_service):
   # Panggil function create_incident untuk menyalakan alur bisnis utama
   incident_service.create_incident(
      title="System crash", 
      description="Main application is down", 
      reported_by="admin@test.com"
   )
   # Cek service memanggil fungsi save() dari repository tepat satu kali
   incident_service.repository.save.assert_called_once()