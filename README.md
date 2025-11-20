# Vensim Web Simulator (Flask + PySD)

A web-based simulation platform developed with **Python (Flask)** and **PySD** that allows users to interact with System Dynamics models originally created in **Vensim**. 

This project specifically demonstrates a case study on **Cargo Transport and Logistics via Tanker Trucks**, allowing users to visualize key variables, run scenarios, and adjust sensitivity parameters in real-time.

## 🚀 Features

- **Web Interface:** Run Vensim models (`.mdl`) directly from a browser without needing the Vensim software installed.
- **Interactive Simulation:** Modify control variables (e.g., Purchase Rate, Sales Rate, Obsolescence) and see immediate results.
- **Dynamic Visualization:** Graphs generated using `Matplotlib` and `mpld3` for interactive data exploration.
- **Database Integration:** Uses **MySQL** to configure graph colors, labels, and display order dynamically.
- **Responsive Design:** Built with **Bootstrap 5** to ensure compatibility with desktops, tablets, and mobile devices.

## 🛠️ Tech Stack

- **Backend:** Python 3.9+, Flask
- **Simulation Engine:** PySD (Python System Dynamics)
- **Database:** MySQL (Connector: `mysql-connector-python`)
- **Frontend:** HTML5, CSS3, Bootstrap 5, Jinja2
- **Plotting:** Matplotlib, mpld3
- **Deployment/Tunneling:** Ngrok (optional for external access)

## 📋 Prerequisites

Ensure you have the following installed on your local machine:

- [Python 3.9.7+](https://www.python.org/)
- [MySQL Server](https://dev.mysql.com/downloads/mysql/) (or XAMPP/WAMP)
- [Git](https://git-scm.com/)

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/MarcOBL012/Simulation-of-a-transport-system-through-system-dynamics.git
cd vensim-flask-simulator
```
### 2. Database Configuration
- Open your MySQL administration tool (e.g., phpMyAdmin or MySQL Workbench).
- Create a new database named vensimweb.
- Import the SQL schema provided in the backup folder:
```
File location: Backup/vensimweb.sql
```
### 3. Environment Variables
Create a .env file in the root directory based on the provided example. Update the database credentials to match your local setup:
```
Ini, TOML

APP_NAME=Vensim
APP_URL_VENSIM=http://localhost/assets/vensim/document.mdl

# Database Configuration
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=vensimweb
DB_USERNAME=root
DB_PASSWORD=your_password
```
### 4. Install Dependencies
It is recommended to use a virtual environment.

```Bash

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate
# Activate it (Mac/Linux)
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 5. Model File Placement
Ensure the Vensim model file (document.mdl) is placed correctly. 
```
The application looks for it in: vensim_python_web/assets/vensim/document.mdl
```
(Note: A backup of the model is available in the Backup/ folder if needed).

### ▶️ Running the Application
To start the local development server:

```Bash
python app.py
Once running, access the dashboard at: http://127.0.0.1:5000/
```
## 📬 Contact
If you use or extend this project, please add a note in the README or contact:

Marco Obispo — marco.obispo.l@uni.pe

