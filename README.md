# Argo Float Dashboard

## Setup and Run Instructions

### Prerequisites
- Node.js (v18 or higher)
- Python (v3.8 or higher)

### 1. Setup Frontend
```bash
cd frontend
npm install
```

### 2. Setup Backend
```bash
# From project root
pip install -r requirements.txt
```

### 3. Run the Application

**Terminal 1 - Start Backend API:**
```bash
python api/api_server.py
# API will run on http://localhost:8061
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm run dev
# Frontend will run on http://localhost:5173
```

### 4. Access the Application
Open your browser and go to: http://localhost:5173

That's it! The frontend will automatically connect to the backend API.
