# PriceCompare - Authentication System Setup

## Project Structure
- **Frontend**: React application (port 3000)
- **Backend**: Flask API (port 5000)
- **Database**: SQLite (`users.db`)

## Backend Setup (Python/Flask)

### Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or install individually:
   ```bash
   pip install flask==2.3.3
   pip install flask-cors==4.0.0
   pip install werkzeug==2.3.7
   ```

2. **Run the Flask server:**
   ```bash
   python app.py
   ```
   
   The backend will start on `http://localhost:5000`

### API Endpoints

#### **POST /api/register**
Register a new user with complete profile information.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe",
  "dob": "1990-01-15",
  "phone": "+1 234 567 8900",
  "address": "123 Main Street",
  "city": "New York",
  "state": "NY",
  "zipCode": "10001",
  "country": "USA"
}
```

**Response (Success - 201):**
```json
{
  "message": "Registration successful",
  "user_id": 1
}
```

**Response (Error):**
- 400: Missing fields, invalid format, age < 13, password < 8 chars
- 409: Email already registered

---

#### **POST /api/login**
Login with email and password.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (Success - 200):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "full_name": "John Doe",
    "email": "user@example.com",
    "phone": "+1 234 567 8900",
    "city": "New York",
    "state": "NY",
    "country": "USA"
  }
}
```

**Response (Error - 401):**
```json
{
  "error": "Invalid email or password"
}
```

---

#### **GET /api/user/<user_id>**
Retrieve complete user profile information.

**Response (Success - 200):**
```json
{
  "user": {
    "id": 1,
    "full_name": "John Doe",
    "email": "user@example.com",
    "date_of_birth": "1990-01-15",
    "phone": "+1 234 567 8900",
    "address": "123 Main Street",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "country": "USA",
    "created_at": "2025-11-17 12:00:00",
    "last_login": "2025-11-17 14:30:00"
  }
}
```

### Database Schema

**users table:**
- `id` - Primary key (auto-increment)
- `full_name` - User's full name
- `email` - Unique email address
- `password_hash` - Hashed password (Werkzeug)
- `date_of_birth` - User's DOB (YYYY-MM-DD)
- `phone` - Contact phone number
- `address` - Street address
- `city` - City name
- `state` - State/Province
- `zip_code` - Postal code
- `country` - Country name
- `created_at` - Registration timestamp
- `last_login` - Last login timestamp

### Validation Rules

- **Email**: Valid email format (RFC 5322)
- **Password**: Minimum 8 characters (hashed with Werkzeug)
- **Age**: Must be at least 13 years old
- **Phone**: Minimum 10 digits (accepts various formats)
- **Date Format**: YYYY-MM-DD

## Frontend Setup (React)

### Installation

1. **Install Node dependencies:**
   ```bash
   npm install
   npm install lucide-react
   ```

2. **Run the React development server:**
   ```bash
   npm start
   ```
   
   The frontend will start on `http://localhost:3000`

### Features

- **Login Form**: Email and password with show/hide toggle
- **Registration Form**: Comprehensive form with personal, address, and security sections
- **Password Strength Indicator**: 5-level strength meter (Very Weak → Strong)
- **Validation**: Client-side validation with server-side backup
- **Error/Success Messages**: Visual feedback with icons
- **Responsive Design**: Works on desktop and mobile devices
- **Icons**: Using lucide-react for UI elements

## Running Both Services

### Terminal 1 - Backend:
```bash
cd pricecomparsion
python app.py
```

### Terminal 2 - Frontend:
```bash
cd pricecomparsion
npm start
```

## Testing

### Test Registration:
1. Click "Register" tab
2. Fill in all fields
3. Password strength meter will show real-time feedback
4. Submit the form
5. Success message should appear

### Test Login:
1. Click "Login" tab
2. Use registered email and password
3. View user data returned from server

## Common Issues

**CORS Error**: Backend Flask-CORS is already configured
**Port Already in Use**: Change port in `app.py` or kill existing process
**Database Locked**: Delete `users.db` to reset (creates new on app restart)
**Import Errors**: Run `pip install -r requirements.txt`

## Notes

- Passwords are hashed using Werkzeug's `generate_password_hash`
- Database uses SQLite for simplicity (upgrade to PostgreSQL for production)
- CORS is enabled for frontend communication
- All data validation occurs both client-side and server-side
