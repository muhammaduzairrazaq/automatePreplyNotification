import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')

def Scrap(link):

    url = link
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    messageClass = "CardSummaryText-sc-1mpm6on-6 dldCOx"
    messages = soup.find_all(class_=messageClass)
    numberMessages = 3
    extractedMessages = [message.get_text().replace('\n', ' ').strip() for message in messages[:numberMessages]]
    return extractedMessages

def sendEmail(mailSubject, mailBody, pageLink):

    sender_email = USERNAME
    receiver_email = "iamprouzair@gmail.com"
    subject = mailSubject
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    body=''
    for i in range(len(mailBody)):
        body += f'{i+1}. {mailBody[i]} \n'
    body += pageLink
    message.attach(MIMEText(body, "plain"))
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = USERNAME
    smtp_password = PASSWORD
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

def readFiles(path):

    returnJobs = []
    if os.path.exists(path):
        with open(path, 'r') as file:
            for line in file:
                line = line.replace('\n', ' ').strip()
                returnJobs.append(line)
    return returnJobs
   
def writeFiles(path, jobList):
    
    if os.path.exists(path):
        with open(path,'w') as file:
            for job in jobList:
                file.write(job)
                file.write('\n')

def execute():

    prevComputerJobs = readFiles('prevComputerJobs.txt')
    prevPythonJobs = readFiles('prevPythonJobs.txt')
    urlComputerJobs = "https://preply.com/en/online/computer-tutoring-jobs"
    urlPythonJobs = "https://preply.com/en/online/python-tutoring-jobs"
    computerJobsToSend = []
    pythonJobsToSend = []
    computerJobsScraped = Scrap(urlComputerJobs)
    pythonJobsScraped = Scrap(urlPythonJobs)
    if computerJobsScraped != prevComputerJobs:
        for cj, pj in zip(computerJobsScraped,prevComputerJobs):
            if cj != pj:
                computerJobsToSend.append(cj)
        sendEmail('Computerscience Jobs', computerJobsToSend, urlComputerJobs)
        writeFiles('prevComputerJobs.txt', computerJobsScraped)
    if pythonJobsScraped != prevPythonJobs:
        for cj, pj in zip(pythonJobsScraped,prevPythonJobs):
            if cj != pj:
                pythonJobsToSend.append(cj)
        sendEmail('Python Jobs', pythonJobsToSend, urlPythonJobs)
        writeFiles('prevPythonJobs.txt', pythonJobsScraped)
    sendEmail('I am running Chill',pythonJobsToSend,urlPythonJobs)
    

if __name__ == "__main__":

   execute()

   