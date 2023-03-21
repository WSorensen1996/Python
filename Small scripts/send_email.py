import smtplib 

email = "...@gmail.com" 
password = "..."

message = "Testing! "

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(email,password)
print("Login succes!")
server.sendmail(email, email, message)
print("Email has been sent to: ", email)
