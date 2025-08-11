# Prasadam Pass

A Django-based event registration and QR check-in system for ISKCON prasadam distribution events in IIT Madras.
Allows devotees to book slots, receive a WhatsApp-confirmation link, and present a QR code at entry.

## ✨ Features

- Devotee registration form with slot selection
- Unique QR code generation per registration
- WhatsApp message link for confirmation
- Volunteer check-in system with QR scanning
- Admin view for tracking attendance

## 🚀 Tech Stack

- Django (all-in-one: backend, frontend, ORM)
- SQLite (locally) /PostgreSQL (prod)
- Python `qrcode` for QR image generation

## env
pip install python -decouple
create .env with SECRET_KEY, DATABASE_URL

