import smtplib 

senderEmail = 'datalogiskekiropraktorer@gmail.com'
password = 'nsgtvpwhxrwrkapp.'


def send_welcome_email(recieverEmail, _id): 
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:  
        email_address = 'datalogiskekiropraktorer@gmail.com'
        email_password = 'nsgtvpwhxrwrkapp'
        connection.login(email_address, email_password )
        connection.sendmail(
            from_addr=email_address, 
            to_addrs=recieverEmail, 
            msg= f"subject: Velkommen til datalogiske kiropraktor \n\n Hej og velkomen til datalogiske kiropraktor - dit login id er {_id}".encode("utf8")
            )

        print("A welcome email has been sent to:  ", recieverEmail)


def send_payout_email(recieverEmail, totalExpenses): 
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:  
        email_address = 'datalogiskekiropraktorer@gmail.com'
        email_password = 'nsgtvpwhxrwrkapp'
        print("Your total expenses are {totalExpenses} - please pay to <4300> <74329347> ".format(totalExpenses=totalExpenses))
        _msg = "subject: Regning fra datalogiske kiropraktor \n\n Din samlede udgifter er {totalExpenses} - du bedes betale dette på <4300> <74329347> ".format(totalExpenses=totalExpenses)
        connection.login(email_address, email_password )
        connection.sendmail(
            from_addr=email_address, 
            to_addrs=recieverEmail, 
            msg= _msg.encode("utf8")
            )

        print("A payout expense email has been send to: ", recieverEmail)



