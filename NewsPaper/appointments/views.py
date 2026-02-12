
from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
from datetime import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from .models import Appointment
from django.core.mail import mail_admins # импортируем функцию для массовой отправки писем админам


# class AppointmentView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'appointments/make_appointment.html', {})
#
#     def post(self, request, *args, **kwargs):
#         appointment = Appointment(
#             date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
#             client_name=request.POST['client_name'],
#             message=request.POST['message'],
#         )
#         appointment.save()
#
#         # отправляем письмо
#         send_mail(
#             subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
#             # имя клиента и дата записи будут в теме для удобства
#             message=appointment.message,  # сообщение с кратким описанием проблемы
#             from_email='n.shirokoradit@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
#             recipient_list=['n.shirokoradit2026@outlook.com',
#                             'ns.shirokorad@gmail.com']  # Cписок получателей.
#         )
#
#         return redirect('appointments:make_appointment')


from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
from datetime import datetime

from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from .models import Appointment


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'appointments/make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # получаем наш html
        html_content = render_to_string(
            'appointments/appointment_created.html',
            {
                'appointment': appointment,
            }
        )

        # в конструкторе уже знакомые нам параметры, да? Называются правда немного по-другому, но суть та же.
        msg = EmailMultiAlternatives(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}', # имя клиента и дата записи будут в теме для удобства
            body=appointment.message,  # это то же, что и message
            from_email='n.shirokoradit@yandex.ru',
            to=['n.shirokoradit2026@outlook.com'],  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылаем

        return redirect('appointments:make_appointment')