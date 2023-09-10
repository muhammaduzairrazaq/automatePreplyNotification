# import requests
# from bs4 import BeautifulSoup
# import time
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import os

# USERNAME = os.environ.get('USERNAME')
# PASSWORD = os.environ.get('PASSWORD')


# # USERNAME = 'iamprouzair@gmail.com'
# # PASSWORD = 'tvusgzrabxuscrud'

# def Scrap(link):

#     try:
#         response = requests.get(link)
#         soup = BeautifulSoup(response.content, 'html.parser')
#         messageClass = "CardSummaryText-sc-1mpm6on-6 dldCOx"
#         messages = soup.find_all(class_=messageClass)
#         numberMessages = 3
#         extractedMessages = [message.get_text().replace('\n', ' ').strip() for message in messages[:numberMessages]]
#         return extractedMessages
    
#     except requests.exceptions.RequestException as e:
#         print(f"Error making the HTTP request: {e}")
#         return []
    
#     except Exception as e:
#         print(f"Error parsing HTML: {e}")
#         return []



# def sendEmail(mailSubject, mailBody, pageLink):

#     sender_email = USERNAME
#     receiver_email = "uzairrazzaq68@gmail.com"
#     subject = mailSubject
#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = receiver_email
#     message["Subject"] = subject

#     body=''
#     for i in range(len(mailBody)):
#         body += f'{i+1}. {mailBody[i]} \n'
#     body += pageLink

#     message.attach(MIMEText(body, "plain"))
#     smtp_server = "smtp.gmail.com"
#     smtp_port = 587
#     smtp_username = USERNAME
#     smtp_password = PASSWORD

#     try:
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls()
#         server.login(smtp_username, smtp_password)
#         server.sendmail(sender_email, receiver_email, message.as_string())
#         server.quit()
#         print('Email sended successfully!')

#     except smtplib.SMTPException as e:
#         print(f'Error: Unable to send email - {e}')
    
#     except Exception as e:
#         print(f'An unexpected error occurred - {e}')


# def readFiles(path):
#     try:
#         returnJobs = []
#         abs_path = os.path.join(os.getcwd(), path)
#         if os.path.exists(abs_path):
#             with open(path, 'r') as file:
#                 for line in file:
#                     returnJobs.append(line.strip()) 
#         return returnJobs
    
#     except FileNotFoundError:
#         print(f'File not found: {path}')
#         return []
#     except Exception as e:
#         print(f'An error occurred while reading the file: {e}')
#         return []
    
# def writeFiles(path, jobList):
    
#     try:
#         abs_path = os.path.join(os.getcwd(), path)
#         if os.path.exists(abs_path):
#             with open(path,'w') as file:
#                 for i, job in enumerate(jobList):
#                     file.write(job)
#                     if i < len(jobList) - 1:
#                         file.write('\n')

#     except FileNotFoundError:
#         print(f'File not found: {path}')
    
#     except Exception as e:
#         print(f'An error occurred while writing the file: {e}')

# def check_for_new_jobs(job_category, url, prev_jobs_file):
#     prev_jobs = readFiles(prev_jobs_file)
#     jobs_to_send = []
#     jobs_scraped = Scrap(url)

#     for job in jobs_scraped:
#         if job not in prev_jobs:
#             jobs_to_send.append(job)

#     if jobs_to_send:
#         sendEmail(job_category, jobs_to_send, url)
#         writeFiles(prev_jobs_file, jobs_scraped)

# def execute():
#     computer_category = 'Computerscience Jobs'
#     python_category = 'Python Jobs'
#     url_computer_jobs = "https://preply.com/en/online/computer-tutoring-jobs"
#     url_python_jobs = "https://preply.com/en/online/python-tutoring-jobs"
    
#     check_for_new_jobs(computer_category, url_computer_jobs, 'prevComputerJobs.txt')
#     check_for_new_jobs(python_category, url_python_jobs, 'prevPythonJobs.txt')

# if __name__ == "__main__":
   
#    execute()
   
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')

def Scrap(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        messageClass = "CardSummaryText-sc-1mpm6on-6 dldCOx"
        messages = soup.find_all(class_=messageClass)
        numberMessages = 3
        extractedMessages = [message.get_text().replace('\n', ' ').strip() for message in messages[:numberMessages]]
        return extractedMessages
    except Exception as e:
        print(f"Error while scraping: {e}")
        return []

def sendEmail(mailSubject, mailBody, pageLink):
    sender_email = USERNAME
    receiver_email = "uzairrazzaq68@gmail.com"
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
        print('Email sent successfully!')

    except smtplib.SMTPException as e:
        print(f'Error: Unable to send email - {e}')
    except Exception as e:
        print(f'An unexpected error occurred - {e}')

def readJobsFromArtifact(artifact_name):
    try:
        artifact_path = os.path.join(os.environ['GITHUB_WORKSPACE'], artifact_name)
        with open(artifact_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f'Artifact not found: {artifact_path}')
        return []
    except Exception as e:
        print(f'An error occurred while reading the artifact: {e}')
        return []

def writeJobsToArtifact(artifact_name, jobList):
    try:
        artifact_path = os.path.join(os.environ['GITHUB_WORKSPACE'], artifact_name)
        with open(artifact_path, 'w') as file:
            for job in jobList:
                file.write(job + '\n')
    except Exception as e:
        print(f'An error occurred while writing the artifact: {e}')


def check_for_new_jobs(job_category, url, prev_jobs_artifact):
    prev_jobs = readJobsFromArtifact(prev_jobs_artifact)
    jobs_to_send = []
    jobs_scraped = Scrap(url)

    for job in jobs_scraped:
        if job not in prev_jobs:
            jobs_to_send.append(job)

    if jobs_to_send:
        sendEmail(job_category, jobs_to_send, url)
        prev_jobs += jobs_scraped
        writeJobsToArtifact(prev_jobs_artifact, prev_jobs)

def execute():
    computer_category = 'Computerscience Jobs'
    python_category = 'Python Jobs'
    url_computer_jobs = "https://preply.com/en/online/computer-tutoring-jobs"
    url_python_jobs = "https://preply.com/en/online/python-tutoring-jobs"
    
    check_for_new_jobs(computer_category, url_computer_jobs, 'previous-computer-jobs')
    check_for_new_jobs(python_category, url_python_jobs, 'previous-python-jobs')

if __name__ == "__main__":
    execute()

