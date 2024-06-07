# -------------ALL REST FRAMEWORK REQS---------
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

#---------------django in app imports----------
from .models import User, Loan, Payment
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from .serializers import newUser, LoanSerializer, PaymentSerializer


#---------------extra import-------------------
# from uuid import UUID
import json

from .ash_task import cc_score


# view for for new user

class newUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = newUser
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # asynchronously function to calulate credit score
            cc_score(user.aadhar_id)

            # response data with uuid for the user
            response_data = {
                'unique_user_id': str(user.aadhar_id),
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # returning error responce for any 
            error_response = {
                'error': serializer.errors
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


# loan application view 
class LoanApplication(generics.CreateAPIView):
    serializer_class = LoanSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        loan_type = request.data.get('loan_type')
        loan_amount = request.data.get('loan_amount')
        interest_rate = request.data.get('interest_rate')
        term_period = request.data.get('term_period')
        disbursement_date_str = request.data.get('disbursement_date')

        try:
            user = User.objects.get(aadhar_id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Check conditions for any denial of loan applicarion
        if user.credit_score is None or user.credit_score < 450:
            return Response({'error': 'Credit score is too low minimum value 450 required.'}, status=status.HTTP_400_BAD_REQUEST)
        if user.annual_income < 150000:
            return Response({'error': 'Total annual income is too low'}, status=status.HTTP_400_BAD_REQUEST)
        if loan_amount > 5000:
            return Response({'error': 'Loan amount exceeds the limit! Make sure to enter correct amount'}, status=status.HTTP_400_BAD_REQUEST)
        if interest_rate < 12:
            return Response({'error': 'Interest rate too low min intereset is 12'}, status=status.HTTP_400_BAD_REQUEST)

        # checking the enterd date correct or not
        try:
            disbursement_date = datetime.strptime(disbursement_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        emi_schedule = self.cust_emiSch(loan_amount, interest_rate, term_period, disbursement_date)

        # Create the loan
        loan = Loan.objects.create(
            user=user,
            loan_type=loan_type,
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            term_period=term_period,
            disbursement_date=disbursement_date,
            emi_schedule=json.dumps(emi_schedule)
        )

        # Calculate EMI schedule
        response_data = {
            'loan_id': str(loan.loan_id),
            'due_dates': emi_schedule
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def cust_emiSch(self, principal, interest_rate, term_period, disbursement_date):
        emi_schedule = []
        rate = interest_rate / 100 / 12
        n = term_period
        emi = principal * rate * (1 + rate) ** n / ((1 + rate) ** n - 1)

        for i in range(1, n + 1): # intial month to last month
            emi_date = disbursement_date + relativedelta(months=i)
            emi_schedule.append({
                'date': emi_date.strftime('%Y-%m-%d'),
                'amount_due': round(emi, 2),
                'paid': False
            })

        return emi_schedule

class MakePayment(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        loan_id = request.data.get('loan_id')
        amount = request.data.get('amount')

        try:
            loan = Loan.objects.get(loan_id=loan_id)
        except Loan.DoesNotExist:
            return Response({'error': 'Loan not found'}, status=status.HTTP_400_BAD_REQUEST)

        if loan.is_closed:
            return Response({'error': 'Loan is already closed'}, status=status.HTTP_400_BAD_REQUEST)

        if Payment.objects.filter(loan=loan, payment_date=date.today()).exists():
            return Response({'error': 'Payment already recorded for today'}, status=status.HTTP_400_BAD_REQUEST)

        emi_schedule = json.loads(loan.emi_schedule)

        unpaid_emis = [emi for emi in emi_schedule if emi['date'] <= date.today().strftime('%Y-%m-%d')  and emi['paid'] == False]
        if unpaid_emis:
            return Response({'error': 'Previous EMIs remain unpaid'}, status=status.HTTP_400_BAD_REQUEST)

        current_emi = next((emi for emi in emi_schedule if emi['date'] == date.today().strftime('%Y-%m-%d')), None)
        if current_emi and current_emi['amount_due'] != amount:
            return Response({'error': 'Payment amount does not match the due installment amount'}, status=status.HTTP_400_BAD_REQUEST)

        Payment.objects.create(loan=loan, amount=amount, is_processed=True)
        self.process_payment(loan, amount, emi_schedule)
        

        response_data = {
            'error': None,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def process_payment(self, loan, amount, emi_schedule):
        total_paid = sum(payment.amount for payment in Payment.objects.filter(loan=loan))
        
        remaining_balance = loan.loan_amount - total_paid

        exces = 0
        exces_check = 0

        for index,emi in enumerate(emi_schedule):
            emi_date = datetime.strptime(emi['date'], '%Y-%m-%d').date() # Getting the date

            
            # updating next amount with according to current payment
            if exces_check == 1:
                emi['amount_due'] -= exces 
                emi['amount_due'] = round(emi['amount_due'], 2) 
                break     
            elif exces_check == -1:
                emi['amount_due'] += exces
                emi['amount_due'] = round(emi['amount_due'], 2) 
                break

            if emi_date >= date.today() and emi['paid'] == False:  # checking that date for date for today
                if amount >= emi['amount_due']:
                    emi['paid'] = True
                    exces = amount - emi['amount_due']
                    exces_check = 1 

                else:
                    exces = emi['amount_due'] - amount
                    exces_check = -1                     
                    emi['paid'] = True

        loan.emi_schedule = json.dumps(emi_schedule)
        loan.save()

        
        if remaining_balance <= 0:
            loan.is_closed = True
            loan.save()


            
class GetStatement(generics.GenericAPIView):
    serializer_class = LoanSerializer

    def get(self, request, *args, **kwargs):
        loan_id = request.query_params.get('loan_id')

        try:
            loan = Loan.objects.get(loan_id=loan_id)
        except Loan.DoesNotExist:
            return Response({'error': 'Loan not found'}, status=status.HTTP_400_BAD_REQUEST)

        #if loan.is_closed:
        #    return Response({'error': 'Loan is already closed'}, status=status.HTTP_400_BAD_REQUEST)


        # Fetch all payments made for the loan
        payments = Payment.objects.filter(loan=loan).order_by('payment_date')

        # Prepare past transactions
        past_transactions = []
        emi_schedule = json.loads(loan.emi_schedule)
        for payment in payments:
            for emi in emi_schedule:
                emi_date = datetime.strptime(emi['date'], '%Y-%m-%d').date()
                if emi_date >= payment.payment_date and payment.is_processed == True:
                    past_transactions.append({
                        'date': payment.payment_date,
                        'principal': emi['amount_due'],
                        'interest': f"{loan.interest_rate}%",  # Display the interest rate
                        'amount_paid': payment.amount
                    })
                    break

        # Prepare upcoming transactions
        upcoming_transactions = []
        for emi in emi_schedule:
            emi_date = datetime.strptime(emi['date'], '%Y-%m-%d').date()
            if emi_date >= date.today() and emi['paid'] == False:
                upcoming_transactions.append({
                    'date': emi['date'],
                    'amount_due': emi['amount_due'],
                    'due': emi['paid']
                })

        response_data = {
            'past_transactions': past_transactions,
            'upcoming_transactions': upcoming_transactions
        }

        return Response(response_data, status=status.HTTP_200_OK)