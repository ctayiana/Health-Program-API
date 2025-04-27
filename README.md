This project helps manage health programs and register clients.
It has two parts:

A console application (for admins to manage clients and programs)

A Flask REST API (for accessing client and program information)

What It Does
Login Protected:
You must enter the password health123 to access the console system.

Manage Clients:
Add, edit, delete, and search for client records. Clients can join one or more health programs.

Manage Health Programs:
Create, update, list, and delete programs easily.

API Access:
Use the API to:

List all clients: /api/v1/clients

See a specific client: /api/v1/client/<client_id>

List all programs: /api/v1/health-programs

Data Storage:
All data is saved in two files:

clients.json for client information

programs.json for health programs

Unique IDs:
Each client and program is assigned a unique ID using UUID.
