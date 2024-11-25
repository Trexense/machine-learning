import google.generativeai as genai

genai.configure(api_key="AIzaSyD5BttzbGAEi41FvoDU61IcDKpZkkdg-P4")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(
    """Mount Batur (Gunung Batur) is an active volcano located at the center of two concentric calderas north west of Mount Agung on the island of Bali, Indonesia. Goa Gajah, or Elephant Cave, is located on the island of Bali near Ubud, in Indonesia. Built in the 9th century, it served as a sanctuary. Bali Zoo is a Large zoo featuring orangutans, elephants & African lions, plus interactive encounters & shows. 
    Based on the Prompt, I want to see animal. Which place i have to go?"""
    )
print(response.text)