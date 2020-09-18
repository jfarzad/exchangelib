from exchangelib import Credentials, Account, UTC_NOW,  EWSTimeZone, EWSDateTime, EWSDate, Q
from collections import defaultdict
from datetime import timedelta, datetime
import requests
from kayako import KayakoAPI
from kayako import Department, TicketCount, TicketStatus, TicketPriority, TicketType, TicketNote, TicketAttachment, Ticket

#Kayako RESTAPI forbindelse
API_URL = 'https://sd.userit.dk/api/index.php'
API_KEY = '981943f6-2b62-7f14-bd25-19017411ec79'
SECRET_KEY = 'MTBlODc5NDMtMjAwOS0yZTY0LTMxNGYtMDI0MTAzZjEwNTVlYjBhZTVlZDctYjk5Mi1jM2U0LWZkYjctMmViZjg4MjBlODM3'
api = KayakoAPI(API_URL, API_KEY, SECRET_KEY)



credentials = Credentials('fmi@userit.dk', 'Bruteforce20')
a = Account('fmi@userit.dk', credentials=credentials, autodiscover=True)
testfolder = a.inbox.parent / 'Test'
since = UTC_NOW() - timedelta(hours=3)
medium = api.first(TicketPriority, title="Medium")
high = api.first(TicketPriority, title="High")
openTicket = api.first(TicketStatus, title="Open")
task = api.first(TicketType, title="Task")
departmentid = 14
timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

#Vi får en report fra TSMportal hver dag imellem 08:45 - 9:30 senest. Der skal laves et cronjob der kører hver dag klokken 9:30.
if not testfolder.filter(subject__icontains='Backup status report', datetime_received__gt=since, sender='info@tsmportal.com').exists():
    ticket = api.create(Ticket, tickettypeid=task.id, ticketstatusid=openTicket.id, ticketpriorityid=high.id, departmentid=departmentid, userid="unassigned")
    ticket.subject = 'TSMPortal [Backup status report] Ikke fundet!' + "\n" + "[" + timestamp + "]"
    ticket.fullname = 'tsmportal'
    ticket.email = 'info@tsmportal.com'
    ticket.contents = "Fix!"
    ticket.add()
    print('Log mangler! Sender kayako ticket....')
else:
    print('Log er fundet.')





