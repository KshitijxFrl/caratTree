from django.urls import path
from .views import newUser, LoanApplication, MakePayment, GetStatement


# custom Urls for all the reuired jobs
urlpatterns = [
    path('api/register-user/', newUser.as_view(), name='register-user'),
    path('api/apply-loan/', LoanApplication.as_view(), name='apply-loan'),
    path('api/make-payment/', MakePayment.as_view(), name='make-payment'),
    path('api/get-statement/', GetStatement.as_view(), name='get-statement'),
]