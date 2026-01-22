# application_for_sending_messages

Веб приложение на Django позволяет пользователям управлять 
рассылками для клиентов. Приложение включает в себя возможность
для создания, просмотра, редактирования и удаления рассылок, а
также отправки сообщений по требованию.

Для запуска данного приложения нужно выполнить в терминале команды:
poetry install,
заполнить данные базы данных,
python manage.py migrate,
Добавьте пользователей командой Выполните команду "python manage.py loaddata users.json --format json".

Пользователи:
admin@example.com
owner@example.com
menager@example.com
user@example.com
Пароли:
1234