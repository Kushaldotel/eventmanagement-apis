# EventMaster Pro 🎉

**Professional Event Management CMS for Modern Organizers**

[![Django](https://img.shields.io/badge/Django-3.2-brightgreen.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-blue.svg)](https://www.django-rest-framework.org/)

A full-featured Event Management Content Management System designed for event companies to efficiently organize, manage, and track events with complete financial and participant management capabilities.

## ✨ Features

### Core Capabilities
- **Complete Event Lifecycle Management**
- **Rich Text Editor (CKEditor 5)** for beautiful event descriptions
- **Multi-user Role Management** (Admins/Staff)
- **Responsive Dashboard** with analytics
- **REST API** for future-proof integration

### 🎯 Event Management
- Create/Edit/Delete events with rich details
- Multiple event categories and tags
- Featured events highlighting
- Event scheduling with date/time management
- Location management with maps integration
- Registration deadline tracking
- Capacity management (max participants)

### 📈 Participant Tracking
- Real-time participant count
- Participant registration records
- Contact information management
- Attendance tracking
- Custom registration forms
- Exportable participant lists (CSV/Excel)

### 💰 Payment Integration
- Secure payment processing (Stripe/Razorpay)
- Multiple payment gateway support
- Registration fee management
- Transaction history tracking
- Payment status monitoring
- Automated receipts/invoices
- Financial reporting

### 📊 Advanced Reporting
- Event performance analytics
- Financial summary reports
- Participant demographic reports
- Attendance rate tracking
- Custom report generation
- Data export capabilities

## 🛠 Technologies Used

**Backend**
- Django 3.2+
- Django REST Framework
- Django CKEditor 5
- PostgreSQL (Recommended)
- Redis (For caching)
- Celery (Async tasks)

**Frontend** (Future Implementation)
- React.js
- Redux Toolkit
- Tailwind CSS
- Chart.js

**Payment Integration**
- Stripe/Razorpay API
- SSL Commerz

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis Server
- Virtualenv

### Installation

1. **Clone Repository**
bash
git clone https://github.com/Kushaldotel/eventmanagement-apis.git
cd eventmaster-pro


2. **Setup Virtual Environment**
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


3. **Install Dependencies**
bash
pip install -r requirements.txt


4. **Configuration**
Create `.env` file:
ini
SECRET_KEY=your-django-secret-key
DEBUG=True
DB_NAME=eventmaster
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
PAYMENT_GATEWAY_KEY=your-payment-api-key


5. **Database Setup**
bash
python manage.py migrate


6. **Create Superuser**
bash
python manage.py createsuperuser


7. **Run Server**
bash
python manage.py runserver
