import pytest
from app.utils.priority_calculator import calculate_priority

def test_priority_high():
   # Mengandung "server down" di title[cite: 1]
   assert calculate_priority("Server down at night", "Need help") == "HIGH"
   # Mengandung "payment failure" di description[cite: 1]
   assert calculate_priority("Issue", "Customer reported payment failure today") == "HIGH"

def test_priority_medium():
   # Mengandung "login" di title[cite: 1]
   assert calculate_priority("Cannot login to system", "Valid credentials used") == "MEDIUM"
   # Mengandung "timeout" di description[cite: 1]
   assert calculate_priority("API issue", "Connection timeout reached") == "MEDIUM"

def test_priority_low():
   # Tidak mengandung kata kunci HIGH atau MEDIUM[cite: 1]
   assert calculate_priority("Change button color", "Make the submit button blue") == "LOW"
   assert calculate_priority("Typo in FAQ", "Fix spelling on page 2") == "LOW"

def test_priority_case_insensitive():
   # Uji case-insensitive untuk HIGH ("SeCuRiTy BrEaCh")[cite: 1]
   assert calculate_priority("Alert", "We have a SeCuRiTy BrEaCh!") == "HIGH"
   # Uji case-insensitive untuk MEDIUM ("ErRoR")[cite: 1]
   assert calculate_priority("eRrOr on page", "Please fix") == "MEDIUM"