import pytest
from app.utils.priority_calculator import calculate_priority

@pytest.mark.parametrize(
   "title, description, expected",
   [
      # Skenario HIGH
      ("Server down at night", "Need help", "HIGH"),
      ("Issue", "Customer reported payment failure today", "HIGH"),
      ("Alert", "We have a SeCuRiTy BrEaCh!", "HIGH"), # Case insensitive
      
      # Skenario MEDIUM
      ("Cannot login to system", "Valid credentials used", "MEDIUM"),
      ("API issue", "Connection timeout reached", "MEDIUM"),
      ("eRrOr on page", "Please fix", "MEDIUM"), # Case insensitive
      
      # Skenario LOW
      ("Change button color", "Make the submit button blue", "LOW"),
      ("Typo in FAQ", "Fix spelling on page 2", "LOW"),
   ]
)

def test_calculate_priority(title, description, expected):
   assert calculate_priority(title, description) == expected