# AbroadMates AI Chatbot

Abroadmates AI is a smart chatbot that helps students get answers about studying abroad—covering visas, tuition, scholarships, accommodation, part-time work, and more. Built with Rasa, it’s your AI-powered study abroad assistant with future plans for avatar chat, document uploads, and personalized student support.

---

## Features

- Built with Rasa 3.6.2
- Understands over 15+ student-related topics:
  - Visa requirements  
  - Accommodation  
  - University selection  
  - Tuition fees  
  - Scholarships  
  - Language requirements  
  - Campus life  
  - Part-time jobs  
  - Internships  
  - Health insurance  
  - Professors and student life
- Future deployment at chatbot.abroadmates.com
- Integrated with Gemini fallback for open-ended queries
- Custom actions using LLMs (Gemini, LLaMA)
- Simple web frontend interface

---
Setup and Run Instructions
1. Create and Activate a Virtual Environment

python3 -m venv rasa_env
source rasa_env/bin/activate
2. Install Dependencies

Make sure you have all required packages installed:

pip install -r requirements.txt
Compatible versions:

rasa==3.6.2
pyyaml==5.4.1
numpy==1.23.5
scikit-learn==1.1.3
tensorflow-macos==2.12.0
python-dotenv==1.1.0
3. Train the Rasa Model

rasa train
4. Start the Chatbot in Shell Mode

rasa shell
5. Start the Action Server

Open a new terminal window, activate your virtual environment again, then:

rasa run actions

## Project Structure

```bash
AbroadMates-Chatbot-Hybrid/
├── actions/                  # Custom Python actions (e.g., Gemini fallback, LLaMA)
│   └── actions.py
├── data/                     # NLU training data and rules
│   ├── nlu.yml
│   └── rules.yml
├── models/                   # Trained Rasa models (.tar.gz)
├── static/                   # Static files (e.g., images, logo)
├── templates/                # (Optional) Frontend templates if used
├── .env                      # Environment variables (e.g., Gemini key)
├── .gitignore                # Files/folders to ignore in version control
├── config.yml                # Rasa pipeline and policy configuration
├── credentials.yml           # Rasa channel credentials
├── domain.yml                # Bot domain: intents, responses, actions
├── endpoints.yml             # Webhook endpoints (e.g., action server)
├── index.html                # Simple chatbot frontend (optional)
├── requirements.txt          # Python dependencies
├── server.py                 # Optional: host chatbot on web
└── README.md                 # You're here 
