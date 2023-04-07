import smtplib
import os
import email.message as message

USERNAME = "kyligalway@gmail.com"
PASSWORD = os.getenv("mail_application_password")


def send_application_email(first_name, last_name, email, start_date, occupation):
    try:
        email_message = message.EmailMessage()
        email_message["Subject"] = "Thank you for your application!"
        message_body = f"""Thank you for your application, {first_name} {last_name}!
    You will hear from us soon!
    Application Data:
        Name: {first_name} {last_name}
        Email: {email}
        Start Date: {start_date.__str__()}
        Current Occupation: {occupation}
    """
        email_message.set_content(message_body)
        print(PASSWORD)
        print(email)
        gmail = smtplib.SMTP("smtp.gmail.com", 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login(USERNAME, PASSWORD)
        gmail.sendmail(USERNAME, email, email_message.as_string())
        gmail.quit()
        return 1
    except Exception as error:
        print("Unable to send email!")
        return 0
