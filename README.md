# Crypto_Graphics
This is a short python3 application that dinamically extracts historical cryptocurrency data from Kraken's REST API and
creates a dashboard using streamlit for visualizing it. 
It also calculates some additional usefull metrics for trading analysis like moving averages or the RSI indicator.

All external libraries used for this project are listed in the requirements.txt file

Installation
------------


You can find a [PyPI package](https://pypi.org/project/Crypto_Graphics/) available.

**Using pip:**

	pip install Crypto_Graphics

**Cloning Repo:**
1) Clone repo to your local directory: 
   
        git clone https://github.com/jmarinMBDS/Crypto_Graphics.git
2) Recreate virtual environment installing all requirements via pip: 
   
        pip install -r Crypto_Graphics\requirements.txt

Launch Application
------------

You can launch the application with the command:
	
    streamlit run Crypto_Graphics\Crypto_dashboard.py 

