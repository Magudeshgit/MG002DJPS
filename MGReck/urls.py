from django.contrib import admin
from django.urls import path, re_path
from authentication import views as avs
from core import views as cvs
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

# PasswordResetView - form for mail
# PasswordResetDoneView - mail sent template
# PasswordResetConfirmView - new password form 
# PasswordResetCompleteView - password reset success view

def ZERROR(request):
    x=2/0
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', avs.home),
    path('TESTING/', ZERROR),

    path('auth/signup/', avs.signup),
    path('auth/signin/', avs.signin),
    path('auth/logout/', avs.logout_user),

    # Core Functionalities
    path('dashboard/', cvs.dashboard),
    path('stocks/', cvs.stocks),
    path('incomingstocks/', cvs.incomingstocks),
    path('damagedmaterials/', cvs.damagedmaterials),

    path('print/', cvs.prindoc),

    path('newbill/', cvs.newbill),
    path('bills/', cvs.bills),
    path('reviewbill/', cvs.reviewbill, name='bill'),
    path('reviewbill/<int:pk>/', cvs.reviewbill, name='bill'),

    path('clientbook/', cvs.clientbook),
    path('laborbook/', cvs.laborbook),

    path('addstock/', cvs.addstock),
    path('editstock/<pk>/', cvs.editstock, name='editstock'),
    path('deletestock/<pk>/', cvs.deletestock, name='deletestock'),

    path('addclient/', cvs.addcustomer),
    path('editclient/<pk>/', cvs.editcustomer, name='editcustomer'),
    path('deletecustomer/<pk>/', cvs.deletecustomer, name='deletecustomer'),

    path('addlabor/', cvs.addlabor),
    path('editlabor/<pk>/', cvs.editlabor, name='editlabor'),
    path('deletelabor/<pk>/', cvs.deletelabor, name='deletelabor'),

    path('attendance/', cvs.attendancemanagement),
    path('attendancerecord/', cvs.attendancerecords),

    path('salarymanagement/', cvs.salarymanagement),
    path('editsalary/<pk>/', cvs.editsalary, name='editsalary'),

    path('printing/<pk>', cvs.testinvoice, name='print'),
    path('print/<pk>/', cvs.printinvoice),

    # Email Verification & Password Reset
    path('activate/<str:uidb64>/<str:token>/', avs.activation, name='activate'),
    path('verificationsuccess/', avs.verificationsuccess),
    path('forgotpassword/mailverification', PasswordResetView.as_view(
        template_name='authentication/passwordresetmailview.html',
        ), name='reset_password'),
    path('forgotpassword/mailsuccess', PasswordResetDoneView.as_view(template_name='authentication/passwordmailsent.html'), name='password_reset_done'),
    path('forgotpassword/newpassword/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name='authentication/passwordresetform.html'), name='password_reset_confirm'),
    path('forgotpassword/resetsuccess', PasswordResetView.as_view(template_name='authentication/passwordresetsuccess.html'), name='password_reset_complete'),

]


