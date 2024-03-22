
# email_classification

Classification of emails based on their importance. Importance is calculated by calculating scores for each email using factors such as sender, subject, words, etc.

Steps to runs the code :
Please make sure you have anaconda and git installed. 


1. Create a new directory and change to that directory. Open terminal. 

2. Use the following commands to set git to the project : 

  ```
  git init
  ```

  ```
  git remote add origin https://github.com/Varad2001/email_classification.git
  ```
  
3. Create new anaconda environment naming 'email_tools'  : 
  
  ```
  conda create -name email_classification
  ```
  
4. Activate the conda env : 
  
  ```
  conda activate email_classification
  ```
  
5. Install pip to the conda env : 
 
 ```
  conda install pip
  ```
  
6. Install the required dependencies : 
 
 ```
  pip install -r requirements.txt
  ```
  
7. Run main.py file : 
  
  ```
  python3 app.py
  ```
