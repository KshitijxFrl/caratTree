# caratTree💎
<div>
  <h4>☀ Cara Tree is top of the loan providing platform which help various users to full their monery need with loan with easy emi options catering their needs. 💸</h4>
</div>

<div>
  <h2>Techinical discption 🚀</h2>
  <h4>▶ This repo contain the backend of the carate tree built with django.</h4>
  <h4>▶ It have four major features and additionaly it comes with a corn job which a job on each day, and fetch the users for whom billing needs to be done. Once the       list of users is available, start the billing process</h4>

  <h3>▶ To access the features here are the apis 🚥</h3>
  <ul>
    <li>To create a new user:- api/register-user/</li>
    <p>Send a POST request with this raw body input </p>
    {
    "aadhar_id": "sameple use id mentioned in the given csv file",<br/>
    "name": "name",<br/>
    "email": "xxx.xxx@example.com",<br/>
    "annual_income": amount <br/>
    }<br/>
    <li>To apply for loan:- api/register-user/</li>
    <p>Send a POST request with this raw body input </p>
    {
    "user": "aadhar id / user id ",<br/>
    "loan_type": "Credit Card",<br/>
    "loan_amount": x,<br/>
    "interest_rate": x,<br/>
    "term_period": x,<br/>
    "disbursement_date": "2024-01-01"<br/>
    }<br/>
    <li>To do a payment of a loan:- api/register-user/</li>
    <p>Send a POST request with this raw body input </p>
    {
    "loan_id": "loan id",<br/>
    "amount": amount which need to be paid<br/>
    }<br/>
    <li>To view a paricular loan dues and past transations:- api/register-user/</li>
    <p>Send a GET request http://127.0.0.1:8000/api/get-statement/?loan_id="Enter Your Loan ID" </p>
  </ul>  
  <h3>To perform Corn Job ⚙</h3>
  <p>A custom billing .py has been made at "credit-services->crs->management->comands->billing" tihs can be performde by bashing python manage.py billing
    or by using corntab in linux or task schdedular in windows.</p>  
</div>

<div>
  <h2>Django app models and view info 📜</h2>
  <h3>Models</h3>
  <ul>
    <li>User: to create a new user</li>
    <li>Loan: to create a loan request</li>
    <li>Payment: for loan transactions</li>
    <li>BillingDetails and DuePayment: for corn jon</li>
  </ul>

  <h3>Views</h3>
  <ul>
    <li>newUser</li>
    <li>LoanApplication</li>
    <li>MakePayment</li>
    <li>GetStatement</li>
  </ul>  
</div>

<div>
  <h2>Additional ⚠</h2>
  <p>To run this api locally make sure to delete the old sqlite db and then re migrate by using "python manage.py makemigration -> python manage.py makemigration" commands</p>
</div>

