from django.core.mail import send_mail
from django.utils import timezone
from mailing_app.models import Mailing, MailingAttempts


def send_mail_recipients(mailing_id):
    """
    Отправляет email получателям
    """
    try:
        mailing = Mailing.objects.get(id=mailing_id)

        mailing.update_status()

        if mailing.status != 'Запущена':
            MailingAttempts.objects.create(
                mailing=mailing.message,
                attempt_time=timezone.now(),
                status='Ошибка',
                server_response=f"Рассылка не активна. Текущий статус: {mailing.status}"
            )
            return

        recipients = mailing.recipients.all()
        success_count = 0
        error_count = 0

        for recipient in recipients:
            try:
                send_mail(
                    subject=mailing.message.letter_subject,
                    message=mailing.message.letter_body,
                    from_email='rafail.shiryaev.2015@mail.ru',
                    recipient_list=[recipient.email],
                    fail_silently=False,
                )

                MailingAttempts.objects.create(
                    mailing=mailing.message,
                    attempt_time=timezone.now(),
                    status='Успешно',
                    server_response=f"Сообщение отправлено на {recipient.email}"
                )
                success_count += 1

            except Exception as e:
                MailingAttempts.objects.create(
                    mailing=mailing.message,
                    attempt_time=timezone.now(),
                    status="Ошибка",
                    server_response=f"Ошибка при отправке на {recipient.email}: {str(e)}"
                )
                error_count += 1

        return {
            'success': success_count,
            'errors': error_count,
            'total': success_count + error_count
        }

    except Mailing.DoesNotExist:
        print(f"Рассылка с ID {mailing_id} не найдена")
        return None
    except Exception as e:
        print(f"Ошибка при отправке рассылки: {str(e)}")
        return None
