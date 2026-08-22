# File: tests/test_notification.py

import pytest
import httpx
from unittest.mock import patch
from app.services.notification_service import send_notification_async

@pytest.mark.asyncio
@patch("app.services.notification_service.httpx.AsyncClient.post")
async def test_notification_service_failure(mock_post, caplog):
    # Setup mock untuk memunculkan TimeoutException (simulasi kegagalan eksternal)
    mock_post.side_effect = httpx.TimeoutException("Connection timed out")

    # Eksekusi fungsi (tidak boleh throw error/crash meskipun gagal)[cite: 1]
    await send_notification_async(incident_id=123)

    # Verifikasi 6: Kegagalan tidak menyebabkan incident gagal, dan tercatat di log[cite: 1]
    assert "Timeout while sending notification for incident 123" in caplog.text