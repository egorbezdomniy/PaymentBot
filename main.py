import random
import string
from datetime import datetime, timedelta
import telebot
import requests
import json
import smtplib
from email.mime.text import MIMEText


def send_email(message, recipient):
    sender = "constantindushin@gmail.com"
    password = "pysa bwga qwrq gskc"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg["Subject"] = "Покупка подписки Мегамаркет Парсинг"
        msg["From"] = sender
        msg["To"] = recipient
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"


bot = telebot.TeleBot('7024765730:AAGqYDBYYk4OiAevixv2Y6IsckJ_YLcAPRM')


def admin_request_post(data):
    credentials = {
        'app_password': 'ERZHNPAss12389!',
        'chat_id': '7777777'
    }
    response = requests.post(url='https://megaparsing.pythonanywhere.com/users/', params=credentials, json=data)
    return response.status_code


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        data = json.loads(message.text)
        email_pon = data.get('email')
        product_names = [product['name'] for product in data.get('payment', {}).get('products', [])]

        if product_names[0] == "Стандарт 30 дней":
            date = datetime.now() + timedelta(days=30)
        elif product_names[0] == "Стандарт 3 месяца":
            date = datetime.now() + timedelta(days=90)
        else:
            date = datetime.now() + timedelta(days=365)

        date_str = date.strftime('%Y-%m-%dT%H:%M:%S')
        data_user = {
            'username': data.get('email'),
            'chat_id': data.get('Login'),
            'subscription_status': True,
            'promo_code': 'Отсутствует',
            'payment_url_1_month': None,
            'payment_url_3_month': None,
            'payment_url_1_year': None,
            'order_id_1_month': None,
            'order_id_3_month': None,
            'order_id_1_year': None,
            'end_of_subscription': date_str,
            'app_password': data.get('Password'),
        }

        status_code = admin_request_post(data_user)

        # Проверка статус-кода
        if status_code == 201:
            print("Все заебись и работало как работает.")
            email_message = f"Здравствуйте!\n Вы успешно купили подписку Мегамаркет Парсинг.\n Ваш логин: " \
                            f"{data.get('Login')}\n Ваш пароль:  {data.get('Password')} \n Скачать программу: https://shorturl.at/iBCDN \n Спасибо за покупку!"
            send_email(email_message, email_pon)
        elif status_code == 400:
            print("Ошибка 400, меняем 'username' и 'chat_id'.")
            # Генерируем новый набор букв и цифр из 12 символов
            new_value = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
            data_user['username'] += new_value
            data_user['chat_id'] += new_value
            # Повторно отправляем данные с новыми значениями
            admin_request_post(data_user)
            email_message = f"Здравствуйте! \nВы успешно купили подписку Мегамаркет Парсинг.\n Ваш логин:" \
                            f" {data_user.get('chat_id')}\n Ваш пароль:  {data.get('Password')} \n Скачать программу: https://shorturl.at/iBCDN \n Спасибо за покупку!"
            send_email(email_message, email_pon)
    except json.JSONDecodeError:
        # Здесь можете добавить логику обработки случаев, когда сообщение не является валидным JSON
        pass

if __name__ == '__main__':
    bot.polling(none_stop=True)
