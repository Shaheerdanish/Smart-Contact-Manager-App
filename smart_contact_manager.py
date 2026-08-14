import json
import re
import shutil
import glob
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List

# 1. EXCEPTIONS (Custom Error Handling)
class InvalidDataError(Exception):
    """Jab user galat email ya phone number daale toh yeh error chalega."""
    pass
# 2. CLASSES (Data Blueprint & Validation)
@dataclass
class Contact:
    name: str
    phone: str
    email: str
    added_on: str = None

    def __post_init__(self):
        # NEW CONTACT ARE ADDED ON TODAY DATE AND TIMESTAMP
        if self.added_on is None:
            self.added_on = datetime.now().strftime("%Y-%m-%d %I:%M %p")
            
    def validate(self):
        # CHECKING EMAIL AND PHONE BY USING REGEX
        if not re.match(r"^\d{4}-\d{7}$", self.phone):
            raise InvalidDataError(f"Phone '{self.phone}' INVALID PHONE FORMATE. (correct: 0300-1234567)")
        
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", self.email):
            raise InvalidDataError(f"Email '{self.email}' valid nahi hai.")

# 3. MAIN APP LOGIC (OS, JSON, Functions)
class SmartContactApp:
    def __init__(self, folder_name: str = "my_contacts_app"):
        # OS & Pathlib: SET THE PATH FOR FOLDERS AND FILES
        self.base_dir = Path.cwd() / folder_name
        self.data_file = self.base_dir / "contacts.json"
        self.backup_dir = self.base_dir / "backups"
        
        # Agar folders nahi hain, toh bana do
        self.base_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        
        self.contacts: List[Contact] = []
        self.load_data()

    def load_data(self):
        """LOAD THE PREVIOUS JSON DATA IN TO THE MEMORY."""
        try:
            if self.data_file.exists():
                with open(self.data_file, "r") as file:
                    data = json.load(file)
                    # CONVERT THE JSON CONTACT DATA IN TO THE OBJECT
                    self.contacts = [Contact(**item) for item in data]
                    print(f"✅ App Started: {len(self.contacts)} contacts load ho gaye.")
            else:
                print("ℹ️ Nayi App Setup ho gayi. Koi purana data nahi mila.")
        except Exception as e:
            print(f"❌ System Error: Data load nahi ho saka -> {e}")

    def add_contact(self, name: str, phone: str, email: str):
        """Naya contact add karta hai aur save karta hai."""
        print(f"\n--- Adding New Contact: {name} ---")
        try:
            # Naya object banana
            new_contact = Contact(name=name, phone=phone, email=email)
            
            # Validation check karna (Yahan Exception aasakti hai)
            new_contact.validate() 
            
            # Agar sab sahi hai toh List mein daalo aur JSON update karo
            self.contacts.append(new_contact)
            self.save_data()
            print(f"🎉 Success! {name} ka data save ho gaya.")
            
        except InvalidDataError as error:
            # User ki ghalti
            print(f"⚠️ Validation Failed: {error}")
        except Exception as error:
            # System ki ghalti
            print(f"❌ System Fault: {error}")

    def save_data(self):
        """Contacts ki list ko JSON mein likhta hai."""
        # Objects ko wapis dictionary mein badalna json dump ke liye
        data_to_save = [asdict(contact) for contact in self.contacts]
        
        with open(self.data_file, "w") as file:
            json.dump(data_to_save, file, indent=4)

    def create_backup(self):
        """Shutil aur Glob use karke files ka backup banata hai."""
        print("\n--- Backup Process Started ---")
        if not self.data_file.exists():
            print("⚠️ Backup ke liye koi data file mojood nahi hai.")
            return

        # Backup file ka naam aaj ke time ke hisaab se rakhna
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_{timestamp}.json"
        backup_path = self.backup_dir / backup_filename
        
        # Shutil se file copy karna
        shutil.copy(self.data_file, backup_path)
        print(f"💾 Backup Ban Gaya: {backup_filename}")
        
        # Glob se check karna ke total kitne backups ho gaye hain
        total_backups = glob.glob(str(self.backup_dir / "*.json"))
        print(f"📂 System mein ab total {len(total_backups)} backups mojood hain.")


# 4. APP KO CHALANA (Execution)
if __name__ == "__main__":
    # App start ki
    app = SmartContactApp()
    
    # 1. correct data (Yeh pass ho jayega)
    app.add_contact(name="Ali Raza", phone="0300-1234567", email="ali.raza@test.pk")
    
    # 2. correct data
    app.add_contact(name="Sara Khan", phone="0333-7654321", email="sara.k@test.pk")
    
    # 3. incorrect data (Exceptions test karne ke liye - yeh reject ho jayega)
    app.add_contact(name="Usman", phone="12345", email="usman-at-test.com")
    
    # 4. Backup Banana
    app.create_backup()