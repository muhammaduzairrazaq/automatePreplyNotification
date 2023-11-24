import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

USERNAME = ''  # Enter sender email.
RECEIVER = ''  # Enter receiver email
PASSWORD = ''  # Enter app password.


def Scrap(link):

    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        messageClass = "CardSummaryText-sc-1mpm6on-6 dldCOx"
        messages = soup.find_all(class_=messageClass)
        numberMessages = 3
        extractedMessages = [message.get_text().replace(
            '\n', ' ').strip() for message in messages[:numberMessages]]
        return extractedMessages

    except requests.exceptions.RequestException as e:
        print(f"Error making the HTTP request: {e}")
        return []

    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return []


def sendEmail(mailSubject, mailBody, pageLink):

    sender_email = USERNAME
    receiver_email = RECEIVER
    subject = mailSubject
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    body = ''
    for i in range(len(mailBody)):
        body += f'{i+1}. {mailBody[i]} \n'
    body += pageLink

    message.attach(MIMEText(body, "plain"))
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = USERNAME
    smtp_password = PASSWORD

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print('Email sended successfully!')

    except smtplib.SMTPException as e:
        print(f'Error: Unable to send email - {e}')

    except Exception as e:
        print(f'An unexpected error occurred - {e}')


def readFiles(path):
    try:
        returnJobs = []
        abs_path = os.path.join(os.getcwd(), path)
        if os.path.exists(abs_path):
            with open(path, 'r') as file:
                for line in file:
                    returnJobs.append(line.strip())
        return returnJobs

    except FileNotFoundError:
        print(f'File not found: {path}')
        return []
    except Exception as e:
        print(f'An error occurred while reading the file: {e}')
        return []


def writeFiles(path, jobList):

    try:
        abs_path = os.path.join(os.getcwd(), path)
        if os.path.exists(abs_path):
            with open(path, 'w') as file:
                for i, job in enumerate(jobList):
                    file.write(job)
                    if i < len(jobList) - 1:
                        file.write('\n')

    except FileNotFoundError:
        print(f'File not found: {path}')

    except Exception as e:
        print(f'An error occurred while writing the file: {e}')


def check_for_new_jobs(job_category, url, prev_jobs_file):
    prev_jobs = readFiles(prev_jobs_file)
    jobs_to_send = []
    jobs_scraped = Scrap(url)

    for job in jobs_scraped:
        if job not in prev_jobs:
            jobs_to_send.append(job)

    if jobs_to_send:
        sendEmail(job_category, jobs_to_send, url)
        writeFiles(prev_jobs_file, jobs_scraped)


def execute():
    computer_category = 'Computerscience Jobs'
    python_category = 'Python Jobs'
    url_computer_jobs = "https://preply.com/en/online/computer-tutoring-jobs"
    url_python_jobs = "https://preply.com/en/online/python-tutoring-jobs"

    check_for_new_jobs(computer_category, url_computer_jobs,
                       'prevComputerJobs.txt')
    check_for_new_jobs(python_category, url_python_jobs, 'prevPythonJobs.txt')


if __name__ == "__main__":

    execute()
