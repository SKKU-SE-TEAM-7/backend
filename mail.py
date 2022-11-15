import smtplib
from email.mime.text import MIMEText
 
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()      # say Hello
smtp.starttls()  # TLS 사용시 필요
smtp.login('smtp.seongyunlee@gmail.com', 'fazzrlmughkedjme')
 
msg = MIMEText('Test smtp')
msg['Subject'] = '인증번호 알림'
msg['To'] = 'mader0708@gmail.com'
smtp.sendmail('noreply.skkuTeam7@skku.edu', 'mader0708@gmail.com', msg.as_string())
 
smtp.quit()