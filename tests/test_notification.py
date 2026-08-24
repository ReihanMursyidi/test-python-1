import pytest
import httpx
from unittest.mock import patch, AsyncMock
from app.services.notification_service import send_notification_async

@pytest.mark.asyncio
async def test_notification_service_failure(caplog):
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        # Paksa metode post tersebut untuk mensimulasikan TimeoutException
        mock_post.side_effect = httpx.TimeoutException("Connection timed out")

        # Eksekusi fungsi (tidak boleh throw error/crash meskipun gagal)[cite: 1]
        await send_notification_async(incident_id=123)

        # Verifikasi bahwa request HTTP sempat dipanggil
        mock_post.assert_called_once_with(
            "http://notification-service/notifications",
            json={"incident_id": 123, "message": "New incident created"},
            timeout=5.0
        )

        # Verifikasi bahwa error tercatat di log
        assert "Timeout while sending notification for incident 123" in caplog.text