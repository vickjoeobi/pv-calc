# PV Financial Calculation

This application is designed to help users model the financial outcomes of investing in a Photovoltaic (PV) Power Plant. It uses `Streamlit` to provide an interactive web interface where users can input various parameters and see the financial projections including Net Present Value (NPV), Levelised Cost of Electricity (LCOE), and more.

## Getting Started

Follow these instructions to get the application running on your local machine for development and testing purposes.

### Prerequisites

Ensure you have Python installed on your system. The application is built and tested with Python 3.8 and above.

### Installation

1. **Clone the repository**  
   First, clone this repository to your local machine using Git.

2. **Install required packages**  
   Navigate to the cloned repository directory and install the required packages listed in `requirements.txt`:

   ```
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**  
   To start the Streamlit application and open up the web interface, run:

   ```
   streamlit run app.py
   ```

   This command will start the server and open the application in your default web browser.

### Usage

- **Web Interface**  
  After running the Streamlit app, the web interface allows you to input various parameters related to the PV Power Plant investment, such as Project Lifetime, Nominal Power, Annual Yield, and more. After inputting your data, the app will display financial metrics including the LCOE, NPV, and potential Return on Investment (ROI).

- **Terminal Testing**  
  If you prefer to test the calculations via terminal or need to perform batch calculations, you can run `python func.py` directly. You can modify the constant variables in `func.py` to test different scenarios.