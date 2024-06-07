# caratTree💎
<div>
  <h3>▶ Cara Tree is top of the loan providing platform which help various users to full their monery need with loan with easy emi options catering their needs. 💸</h3>
</div>

<div>
  <h2>Techinical discption 🚀</h2>
  <h3>▶ This repo contain the backend of the carate tree built with django.</h3>
  <h3>▶ It have four major features and additionaly it comes with a corn job which a job on each day, and fetch the users for whom billing needs to be done. Once the       list of users is available, start the billing process</h3>

  <h3>▶ To access the features here are the apis 🚥</h3>
  <ul>
    <li>To create a new user:- api/register-user/</li>
    <p>Send a POST request with this raw body input </p>
    {<br />
    "aadhar_id": "56f5dda0-a270-4b41-a772-fd40abbe1e5c",
    "name": "J",
    "email": "jjjj.xyz@example.com",
    "annual_income": 1500000
    }


  <ul>
    <li>To create a new loan application/ loan :- api/register-user/</li>
    <p>Send a POST request with this raw body input </p>
  </ul>
  <ul>
    <li>To do a payment of a loan:- api/register-user/</li>
    <p>Send a POST request with this raw body input </p>
    
  </ul>
  <ul>
    <li>To view a paricular loan dues and past transations:- api/register-user/</li>
    <p>Send a GET request http://127.0.0.1:8000/api/get-statement/?loan_id="Enter Your Loan ID" </p>
  </ul>  
  <h3>To perform Corn Job ⚙</h3>
  <p>A custom billing .py has been made at "credit-services->crs->management->comands->billing" tihs can be performde by bashing python manage.py billing
    or by using corntab in linux or task schdedular in windows.</p>
  
</div>
