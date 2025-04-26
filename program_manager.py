import json
from dataclasses import dataclass, asdict, field
from datetime import datetime
import uuid

# --- PASSWORD PROTECTION ---
SYSTEM_PASSWORD = "health123"  # Set your system password here

def authenticate():
    attempts = 3
    while attempts > 0:
        entered_password = input("Enter system password: ").strip()
        if entered_password == SYSTEM_PASSWORD:
            print("\nAccess granted.\n")
            return True
        else:
            attempts -= 1
            print(f"Incorrect password. {attempts} attempt(s) remaining.\n")
    print("Access denied. Exiting program.")
    return False

# --- HEALTH PROGRAM CLASSES ---
@dataclass
class HealthProgram:
    name: str
    description: str = ""
    program_id: str = None
    created_at: datetime = None
    
    def __post_init__(self):
        self.program_id = self.program_id or str(uuid.uuid4())
        self.created_at = self.created_at or datetime.now()

    def display(self):
        return f"{self.name} ({self.program_id[:8]}): {self.description}"

class ProgramManager:
    def __init__(self, storage_file="programs.json"):
        self.storage_file = storage_file
        self.programs = []
        self.load_programs()

    def add_program(self, name, description=""):
        if not name.strip():
            raise ValueError("Program name cannot be empty")
        new_program = HealthProgram(name.strip(), description.strip())
        self.programs.append(new_program)
        self.save_programs()
        return new_program

    def edit_program(self, program_id, new_name=None, new_description=None):
        for program in self.programs:
            if program.program_id.startswith(program_id):
                if new_name:
                    program.name = new_name.strip()
                if new_description:
                    program.description = new_description.strip()
                self.save_programs()
                return program
        return None

    def delete_program(self, program_id):
        self.programs = [p for p in self.programs if not p.program_id.startswith(program_id)]
        self.save_programs()

    def list_programs(self):
        return [program.display() for program in self.programs]

    def save_programs(self):
        with open(self.storage_file, 'w') as f:
            json.dump([asdict(p) for p in self.programs], f, indent=2, default=str)

    def load_programs(self):
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                self.programs = [
                    HealthProgram(
                        name=p['name'],
                        description=p['description'],
                        program_id=p['program_id'],
                        created_at=datetime.fromisoformat(p['created_at'])
                    ) for p in data
                ]
        except (FileNotFoundError, json.JSONDecodeError):
            self.programs = []

# --- CLIENT CLASSES ---
@dataclass
class Client:
    full_name: str
    age: int
    gender: str
    program_ids: list = field(default_factory=list)
    client_id: str = None
    registered_at: datetime = None

    def __post_init__(self):
        self.client_id = self.client_id or str(uuid.uuid4())
        self.registered_at = self.registered_at or datetime.now()

    def display(self, program_names=[]):
        programs = ", ".join(program_names) if program_names else "No programs"
        return f"{self.full_name} ({self.age}, {self.gender}) - Programs: {programs} (ID: {self.client_id[:8]})"

class ClientManager:
    def __init__(self, storage_file="clients.json"):
        self.storage_file = storage_file
        self.clients = []
        self.load_clients()

    def register_client(self, full_name, age, gender, program_ids):
        if not full_name.strip():
            raise ValueError("Client name cannot be empty")
        if age <= 0:
            raise ValueError("Age must be positive")
        if gender.lower() not in ('male', 'female', 'other'):
            raise ValueError("Gender must be Male, Female, or Other")

        new_client = Client(full_name.strip(), age, gender.strip().capitalize(), program_ids)
        self.clients.append(new_client)
        self.save_clients()
        return new_client

    def edit_client(self, client_id, new_full_name=None, new_age=None, new_gender=None, new_program_ids=None):
        for client in self.clients:
            if client.client_id.startswith(client_id):
                if new_full_name:
                    client.full_name = new_full_name.strip()
                if new_age is not None:
                    client.age = new_age
                if new_gender:
                    client.gender = new_gender.strip().capitalize()
                if new_program_ids is not None:
                    client.program_ids = new_program_ids
                self.save_clients()
                return client
        return None

    def delete_client(self, client_id):
        self.clients = [c for c in self.clients if not c.client_id.startswith(client_id)]
        self.save_clients()

    def list_clients(self, programs):
        program_dict = {p.program_id: p.name for p in programs}
        return [
            client.display([program_dict.get(pid, "Unknown") for pid in client.program_ids])
            for client in self.clients
        ]

    def search_clients(self, keyword, programs):
        keyword = keyword.lower()
        program_dict = {p.program_id: p.name for p in programs}
        results = [
            client.display([program_dict.get(pid, "Unknown") for pid in client.program_ids])
            for client in self.clients
            if keyword in client.full_name.lower()
        ]
        return results

    def get_client_by_id(self, client_id):
        for client in self.clients:
            if client.client_id.startswith(client_id):
                return client
        return None

    def save_clients(self):
        with open(self.storage_file, 'w') as f:
            json.dump([asdict(c) for c in self.clients], f, indent=2, default=str)

    def load_clients(self):
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                self.clients = [
                    Client(
                        full_name=c['full_name'],
                        age=c['age'],
                        gender=c['gender'],
                        program_ids=c.get('program_ids', []),
                        client_id=c['client_id'],
                        registered_at=datetime.fromisoformat(c['registered_at'])
                    ) for c in data
                ]
        except (FileNotFoundError, json.JSONDecodeError):
            self.clients = []

# --- MAIN PROGRAM FUNCTIONS ---
def display_menu():
    print("\nHealth Program Manager")
    print("1. Create new program")
    print("2. View all programs")
    print("3. Register new client (enroll in multiple programs)")
    print("4. View all clients")
    print("5. View a client's profile")
    print("6. Search for a client")
    print("7. Edit a program")
    print("8. Delete a program")
    print("9. Edit a client")
    print("10. Delete a client")
    print("11. Exit")

def main():
    if not authenticate():
        return  

    program_manager = ProgramManager()
    client_manager = ClientManager()

    while True:
        display_menu()
        choice = input("Enter your choice (1-11): ")

        if choice == "1":
            try:
                name = input("Enter program name: ")
                description = input("Enter description (optional): ")
                program = program_manager.add_program(name, description)
                print(f"Successfully created: {program.display()}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            print("\nCurrent Health Programs:")
            if not program_manager.programs:
                print("No programs available yet.")
            else:
                for i, program in enumerate(program_manager.list_programs(), 1):
                    print(f"{i}. {program}")

        elif choice == "3":
            if not program_manager.programs:
                print("No programs available yet. Create a program first.")
                continue
            try:
                full_name = input("Enter client's full name: ")
                age = int(input("Enter client's age: "))
                gender = input("Enter client's gender (Male/Female/Other): ")

                print("\nAvailable Programs:")
                for idx, program in enumerate(program_manager.programs, 1):
                    print(f"{idx}. {program.name} ({program.program_id[:8]})")

                selections = input("Select programs by numbers (comma-separated, e.g., 1,3): ")
                selection_indices = [int(i.strip()) - 1 for i in selections.split(",")]
                selected_program_ids = [program_manager.programs[i].program_id for i in selection_indices]

                client = client_manager.register_client(full_name, age, gender, selected_program_ids)
                program_names = [program_manager.programs[i].name for i in selection_indices]
                print(f"Successfully registered client: {client.display(program_names)}")
            except (ValueError, IndexError) as e:
                print(f"Error: {e}")

        elif choice == "4":
            print("\nRegistered Clients:")
            if not client_manager.clients:
                print("No clients registered yet.")
            else:
                for i, client in enumerate(client_manager.list_clients(program_manager.programs), 1):
                    print(f"{i}. {client}")

        elif choice == "5":
            client_id = input("Enter client's ID (first few characters are enough): ").strip()
            client = client_manager.get_client_by_id(client_id)
            if client:
                program_dict = {p.program_id: p.name for p in program_manager.programs}
                enrolled_programs = [program_dict.get(pid, "Unknown Program") for pid in client.program_ids]
                print("\nClient Profile:")
                print(f"Full Name: {client.full_name}")
                print(f"Age: {client.age}")
                print(f"Gender: {client.gender}")
                print(f"Registered At: {client.registered_at.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Enrolled Programs: {', '.join(enrolled_programs) if enrolled_programs else 'No programs enrolled'}")
            else:
                print("Client not found with that ID.")

        elif choice == "6":
            keyword = input("Enter name or part of the name to search: ").strip()
            results = client_manager.search_clients(keyword, program_manager.programs)
            if results:
                print("\nSearch Results:")
                for i, client_info in enumerate(results, 1):
                    print(f"{i}. {client_info}")
            else:
                print("No clients found matching that search term.")

        elif choice == "7":
            program_id = input("Enter program ID (first few characters): ").strip()
            new_name = input("Enter new program name (leave blank to keep current): ").strip()
            new_description = input("Enter new description (leave blank to keep current): ").strip()
            updated_program = program_manager.edit_program(program_id, new_name if new_name else None, new_description if new_description else None)
            if updated_program:
                print(f"Program updated successfully: {updated_program.display()}")
            else:
                print("Program not found.")

        elif choice == "8":
            program_id = input("Enter program ID to delete (first few characters): ").strip()
            program_manager.delete_program(program_id)
            print("Program deleted successfully.")

        elif choice == "9":
            client_id = input("Enter client ID (first few characters): ").strip()
            client = client_manager.get_client_by_id(client_id)
            if not client:
                print("Client not found.")
                continue

            new_name = input("Enter new full name (leave blank to keep current): ").strip()
            new_age = input("Enter new age (leave blank to keep current): ").strip()
            new_gender = input("Enter new gender (leave blank to keep current): ").strip()

            print("\nAvailable Programs:")
            for idx, program in enumerate(program_manager.programs, 1):
                print(f"{idx}. {program.name} ({program.program_id[:8]})")
            selections = input("Select programs by numbers (comma-separated) or leave blank to keep current: ").strip()
            if selections:
                selection_indices = [int(i.strip()) - 1 for i in selections.split(",")]
                selected_program_ids = [program_manager.programs[i].program_id for i in selection_indices]
            else:
                selected_program_ids = None

            updated_client = client_manager.edit_client(
                client_id,
                new_full_name=new_name if new_name else None,
                new_age=int(new_age) if new_age else None,
                new_gender=new_gender if new_gender else None,
                new_program_ids=selected_program_ids
            )
            print(f"Client updated successfully: {updated_client.display()}")

        elif choice == "10":
            client_id = input("Enter client ID to delete (first few characters): ").strip()
            client_manager.delete_client(client_id)
            print("Client deleted successfully.")

        elif choice == "11":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 11.")

if __name__ == "__main__":
    main()