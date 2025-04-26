# Health Program Management API

- **Method:** GET
- **URL:** `/api/v1/clients`
- **Response:** List of clients

### Get Client By ID
- **Method:** GET
- **URL:** `/api/v1/client/<client_id>`
- **Response:** Client details or 404 if not found

### Get All Health Programs
- **Method:** GET
- **URL:** `/v1/health-programs`
- **Response:** List of available health programs

---

## Error Responses
- **404 Not Found:** Resource not found
- **400 Bad Request:** Invalid request format
