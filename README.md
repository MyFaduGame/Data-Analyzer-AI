Roverin Event Micro Service

**Dependencies**

1. Python 3.11.3


**Run the project**

 1.Create virtual environment with python3.11.3
 
   ```
   python3.11 -m venv venv
   ```

 2.Activate the virtual environment
 
  ```
  source venv/bin/activate
  ```
 
 3.Install the requirements
 
  ```
  pip install -r requirements.txt
  ```
 
 4.Update the .env with corresponding values
 
 5.Run the server
  ```
  uvicorn src.main:app
  ```

