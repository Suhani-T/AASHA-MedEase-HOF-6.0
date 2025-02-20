# AASHA-MedEase-HOF-6.0
A project developed for HackoFiesta 6.0 - AISpire UP Hackathon, providing AI-powered real-time queue management for doctor appointments. The system predicts patient waiting times using machine learning models and integrates seamlessly into a web platform for efficient scheduling.

## Key Features
- **Predicted Waiting Time**: Displays estimated waiting time and the number of patients ahead.
- **AI Chatbot**: Provides instant responses to medical queries.
- **Online Appointment Booking**: Patients can easily book appointments with available doctors.

## Installation & Setup
Follow these steps to set up and run the project:

1. **Install Python** (if not already installed).
2. **Clone the Repository**:
   ```bash
   git clone https://github.com/Suhani-T/AASHA-MedEase-HOF-6.0
   ```
3. **Navigate to the Project Directory**:
   ```bash
   cd AASHA-MedEase-HOF-6.0
   cd hof_project
   ```
4. **Set Up Virtual Environment**:
   - **Delete** the cloned `myenv` environment (if present).
   - Create a new virtual environment:
     ```bash
     python -m venv myenv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```bash
       myenv\Scripts\activate
       ```
     - On macOS/Linux:
       ```bash
       source myenv/bin/activate
       ```
5. **Install Dependencies**:
   ```bash
   cd aasha_project
   pip install -r requirements.txt
   ```
6. **Run the Server**:
   ```bash
   python manage.py runserver
   ```
7. **Access the Website**:
   - Click on the generated link (e.g., `http://127.0.0.1:8000/`) and navigate through the platform!

## Future Enhancements
- **Prescription History**: Patients can access previous prescriptions.
- **Doctor Notes**: Doctors can save important notes for each patient.
- **Billing & Payment Integration**: Secure online payments for appointments.

---
AASHA-MedEase is an ongoing project aimed at **simplifying healthcare management** and improving patient experience.

