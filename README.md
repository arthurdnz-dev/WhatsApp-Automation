WhatsApp Automation System — Python + Selenium

A modular, scalable, and production-oriented automation tool for sending WhatsApp campaigns using Python, Selenium, and structured templates.
Designed for companies, freelancers, and marketing teams that need a fast, customizable, and highly maintainable automation solution.


Overview:

This project is a fully modular WhatsApp messaging automation system capable of:
Loading contacts from CSV files
Running marketing/operational campaigns
Using message templates (welcome, billing, promotion, etc.)
Supporting custom messages per contact
Logging all sent messages
Running in production mode or dry-run mode
Easy to customize for different companies or clients
Written with a clean and scalable architecture



This structure allows the project to grow into:

An API
A GUI app
A multi-platform automation tool
A SaaS messaging system


Features:

Automated WhatsApp Messaging
Uses Selenium to open WhatsApp Web and automatically:
Navigate to contacts
Open a chat
Send messages
Send media (future)
Apply human-like delays



Message Templates
Current templates:

boas_vindas — Welcome message
cobranca — Billing/reminder message
divulgacao — Marketing announcement
You can easily add templates by editing src/core/templates.py.



Contact Management
Reads a structured CSV in the format:

name,phone,message
John Doe,5511999999999,Hello John, your invoice is ready.
...


Dry-Run Mode
Enable test mode in .env:

DRY_RUN=True



Cross-Company Adaptation
The system was built to be easily customized for:

Brazilian companies
International companies
Marketing agencies
Customer support teams
Automation freelancers


Installation
1- Clone the repository:
git clone https://github.com/arthurdnz-dev/WhatsApp-Automation.git
cd automation-pro

2- Create a virtual environment
python -m venv venv

3- Activate it
Windows:
venv\Scripts\activate

4- Install dependencies
pip install -r requirements.txt

5- Create your .env file
PROFILE_PATH=""
DRY_RUN=False

6- How to Run
python main.py


Use Cases:

- Companies
Customer onboarding
Billing reminders
Service confirmations
Announcements/promo blasts

- Freelancers
Client follow-up
Portfolio presentation
Business proposals

- Sales Teams
Re-engagement
Pre-sales messages
Cold outreach (legal guidelines apply)


Roadmap (Future Enhancements):
Rich media sending (images, PDFs, videos)
Campaign statistics dashboard
GUI desktop version (Tkinter/PySide)
API version for enterprise use
AI dynamic message generation
Scheduled campaigns
Contact grouping system


This project is licensed under the MIT License - free for personal and commercial use.
