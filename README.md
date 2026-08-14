# 📱 Smart Contact Manager & Auto-Backup System

An advanced Python console application for securely managing contacts, with built-in validation and automatic timestamped backups in JSON format.

## ✨ Features

- **Object-Oriented Architecture:** Built with dataclasses for clean, structured data modeling.
- **Smart Validation:** Regex-based verification for phone numbers and email addresses.
- **Auto-Backup Engine:** Automated timestamped backups using `shutil` and `glob`.
- **Graceful Error Handling:** Custom exceptions ensure the system fails safely without crashing.

## 🚀 Getting Started

1. Clone the repository:
```bash
   git clone https://github.com/yourusername/smart-contact-manager.git
```
2. Navigate to the project folder:
```bash
   cd smart-contact-manager
```
3. Run the application:
```bash
   python app.py
```

## 📁 Data Storage

On first run, the app automatically creates a `my_contacts_app` folder containing `contacts.json` and a `backups/` directory. All data is stored locally and is not uploaded to GitHub.