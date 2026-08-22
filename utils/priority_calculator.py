def calculate_priority(title: str, description: str) -> str:
   combined_text = f"{title} {description}".lower()

   high_keywords = ["server down", "database down", "payment failure", "security breach"]
   medium_keywords = ["login", "slow", "timeout", "error"]

   for keyword in high_keywords:
      if keyword in combined_text:
         return "HIGH"

   for keyword in medium_keywords:
      if keyword in combined_text:
         return "MEDIUM"

   return "LOW"