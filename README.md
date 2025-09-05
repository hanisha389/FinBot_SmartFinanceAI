# FinBot 
A smart chatbot which is use to answer all your finance related questions 
have a look at the model here
``` https://drive.google.com/drive/folders/13gvkcU3s_dvxXb2NntQ8QbpIicfUjKs8 ```

## Overview  
It consists of a clean register and login page 
- Chatbot page with a student and professional mode for different ways of answer
- Task page which gives you daily and weekly task to save money and in return gives you level points 
- Graphical representation of it and a leaderboard system to track your savings with your friends 
- A Simple Loan calculator to help you calculate loans for your bike , car , home 
- Stock viewer which lets you view the stock of your choice provides a graphical representation of the Stock 

## Tech Stack
- python(Transformers , Google generativeAI , pandas)
- Matplotlib for graphs
- Streamlit for frontend

## Installation 
1. Clone the repo  
   ```
   git clone https://github.com/Kartikey5853/SmartFinanceAI_Finbot
   cd SmartFinanceAI_Finbot
    ```
2. Install the requirements of the project   
    ```pip install -r requirements.txt```

3.Run the program
   - run the main.py file to use the gemini version of the project(recommened)
      
        ``` streamlit run main.py```
    enter your gemini key in line

    ```13     api_key = "" ```
   - run the main2.py file to use the IBM Granite-4-0-tiny model 
        ``` streamlit run main2.py```
    enter your hugging face token in line 
    ```13 HUGGING_FACE_TOKEN = "" ```

## Contributors  
- **Kartikey**: Backend logic , gamification of savings.  
- **Hanisha**: Frontend UI, styling, Stock System, Presentation Prepration.  

    
