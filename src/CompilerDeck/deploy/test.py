import smtplib
from email.mime.text import MIMEText

subject   = 'This is a test'
message   = 'Of the emergency broadcast system. In the event of an actual emergency...'
sender    = 'scott@lettermotion.com'
recipient = 'scott@lettermotion.com'
host      = 'smtpout.secureserver.net'
port      = 25

msg            = MIMEText(message)
msg['Subject'] = subject
msg['From']    = sender
msg['To']      = recipient

s = smtplib.SMTP()
s.set_debuglevel(True)
s.connect(host, port)
print 'Connection active'
s.login('scott@lettermotion.com', 'chavez79')
print 'Login complete'
#s.starttls()
#print 'TLS Started'
s.sendmail(sender, [recipient], msg.as_string())
print 'Email sent'
s.quit()
print 'Mail Operation Complete'
