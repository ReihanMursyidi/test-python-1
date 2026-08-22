import httpx
import logging

# Config logger
logger = logging.getLogger(__name__)

async def send_notification_async(incident_id: int):
   url = "http://notification-service/notifications"
   payload = {
      "incident_id": incident_id,
      "message": "New incident created"
   }

   async with httpx.AsyncClient() as client:
      try:
         response = await client.post(url, json=payload, timeout=5.0)
         response.raise_for_status()
         logger.info(f"Notification sent successfully for incident {incident_id}")

      except httpx.TimeoutException:
         logger.error(f"Timeout while sending notification for incident {incident_id}")
      except httpx.RequestError as exc:
         logger.error(f"An error occurred while requesting {exc.request.url!r}.")
      except Exception as e:
         logger.error(f"Unexpected error sending notification: {str(e)}")