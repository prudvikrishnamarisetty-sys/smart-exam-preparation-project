# Smart Examination Platform

An AI-driven educational platform designed for B.Tech and government exam aspirants. This platform provides a robust, interactive environment for taking exams, featuring real-time AI question sourcing, comprehensive result analytics, and an intuitive admin dashboard for managing resources and configurations.

## Features

* **AI-Powered Question Generation**: Utilizes Google GenAI to dynamically generate exam questions and study notes based on defined configurations and official exam patterns.
* **Interactive Exam Environment**: A responsive frontend built with React, featuring secure, timed exam sessions and an AI assistant for step-by-step solutions and explanations.
* **Admin Dashboard**: Comprehensive tools for live data syncing, resource uploading, database fallback management, and configuring exams.
* **User Authentication**: Secure JWT-based authentication system with encrypted passwords using `bcrypt`.
* **Analytics and Results**: Detailed post-exam analytics using `recharts` to track performance metrics and visualize progress.

## Technology Stack

* **Backend**: FastAPI (Python), SQLAlchemy, Uvicorn, SQLite
* **Frontend**: React 18, Vite, React Router, Recharts, Lucide React
* **AI Integration**: Google GenAI

## Prerequisites

* Python 3.10+
* Node.js (v18 or higher)
* A valid Google GenAI API Key (configured in `.env`)

## Installation and Setup

1. **Clone or Download the Repository**
   Navigate to the project directory in your terminal.

2. **Configure Environment Variables**
   Create a `.env` file in the root directory (you can use `.env.example` as a template) and add your AI credentials and other secrets:
   ```env
   GEMINI_API_KEY="your-google-genai-api-key"
   SECRET_KEY="your-secret-key-for-jwt"
   ```

3. **Running the Application (Windows)**
   The project includes a convenient batch script to set up and run both the backend and frontend simultaneously.
   Simply execute the `run_project.bat` file from the root directory:
   ```bash
   run_project.bat
   ```
   *This script will automatically create a Python virtual environment, install backend dependencies, install frontend `node_modules`, and launch both servers in separate windows.*

4. **Manual Startup**
   If you prefer to run the components manually:

   * **Backend**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     pip install -r requirements.txt
     python main.py
     ```
     The FastAPI backend will typically be accessible at `http://localhost:8000`.

   * **Frontend**:
     ```bash
     npm install
     npm run dev
     ```
     The Vite React app will be accessible at the URL provided in the terminal (usually `http://localhost:5173`).

## Project Structure

* `main.py` / `routers/` / `services/`: FastAPI backend application logic, routing, and core services.
* `models.py` / `schemas.py` / `database.py`: SQLAlchemy database models, Pydantic validation schemas, and database connection.
* `src/`: React frontend application source code.
* `exam.db`: SQLite database for storing users, exams, resources, and configurations.
* `seed_exam_configs.py` / `seed_questions.py`: Utility scripts for populating the database with initial configurations and sample questions.
* `run_project.bat`: One-click startup script for Windows environments.
