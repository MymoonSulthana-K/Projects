import random
import csv
from tkinter import*
root=Tk()
import sys

root.title('Alpha Bank')
color = sys.stdout.shell

def writefile(file):  #New user for online ac
    print("\n\t\t\t\t\t\tWelcome to Alpha Bank")
    print("\t\t\t\t\t\t\t-Banking at your fingertips")
    color.write("\t\t\t\t\t\tCreate your username and password","SYNC")
    print()
    writer=csv.writer(file)
    uname=input("\tEnter the username:")
    password=input("\tEnter the password:")
    print()
    data=[uname,password]
    writer.writerow(data)
    color.write("\tYou have created your account successfully!","STRING")
    
def write(l):
    file=open('Details.csv','a+',newline='')
    writer=csv.writer(file)
    writer.writerow(l)
    file.close()

def readdata():
    file=open('Details.csv','r')
    reader=csv.reader(file)
    for row in reader:
        ac_name=row[0]
        print('\n\tAccount Name:',row[0])
        print('\tDOB:',row[1])
        print('\tGender:',row[2])
        print('\tAccount No:' ,row[3])
        print('\tAccount Type:',row[4])
        print('\tIFSC:',row[5])
        print('\tPlace:',row[6])
        print('\tPhone no:',row[7])
    
def setup():#For Setting up online account
    print("\t\t\t\t\t\tWelcome to Alpha Bank")
    print("\t\t\t\t\t\t\t-Banking at your fingertips")
    print()
    color.write("\t\t\t\t\t\tEnter your details","SYNC")
    ac_name=input("\n\tName of the A/c holder:")
    dob=input("\tDate of birth:")
    gender=input("\tGender:")
    ac_no=input("\tEnter your ac_no:")
    acctype=input("\tEnter the account type:")
    ifsc=input("\tEnter your ifsc code:")
    place=input('\tEnter your address:')
    phno=input("\tEnter your phone no:")
    l=[ac_name,dob,gender,ac_no,acctype,ifsc,place,phno]
    color.write("\t\t\t\t\t\tWe have sent you an otp number\t\t\t\t\t\t","hit")           
    widget=Label(root, text=''' ALPHA BANK\n\t\t\t-Banking at your fingertips\nYour OTP:''')
    number=random.randint(100,999)
    showotp=Label(root, text=number)
    widget.pack()
    showotp.pack()
    root.mainloop()
    enter=int(input("\n\tEnter the otp sent to your registered phone number:"))
    if enter==number:
        file=open('info.csv','a+',newline='')
        writefile(file)
        write(l)
        file.close()
        home()
    else:
        color.write("\tYour otp is invalid\n","COMMENT")
        setup(file)
    
    
def superhome():  #Home Page
    print("\t\t\t\t\t\tWelcome to Alpha Bank")
    print("\t\t\t\t\t\t\t-Banking at your fingertips")
    print()
    print("\t1.Login to your account\n\t2.Set up your online banking account")
    choice=int(input('\tEnter 1 or 2:'))
    return choice

def logout():           #logout
    y=(input("\tDo you want to log out of your account[y/n]:"))
    if y=='y':
        print()
        m=superhome()
        if m==1:
            print(home())
        else:
            print(setup(file))

def cat():
    while True:#Category
        print("\n\t\t\t\t\t\tWelcome to Alpha Bank")
        print("\t\t\t\t\t\t\t-Banking at your fingertips")
        color.write("\t\t\t\t\t\tYour Dashboard","SYNC")
        print()
        print('''                 1.Account Details
                 2.Make Transactions
                 3.Payments History
                 4.Logout''')
        print()
    
        ch=int(input('\tEnter your choice:'))
        if ch==1:
            ac_details()
        elif ch==2:
            bill()
        elif ch==3:
            transact()
        elif ch==4:
            n=logout()
            print(n)
        else:
            color.write("\tWrong choice","COMMENT")

def ac_details(): #When account details is clicked
    print("\n\t\t\t\t\t\tWelcome to Alpha Bank")
    print("\t\t\t\t\t\t\t-Banking at your fingertips")
    color.write("\t\t\t\t\t\tAccount details","SYNC")
    print()
    ac_no=input('\tEnter your account number:')
    file=open('Details.csv','r')
    reader=csv.reader(file)
    for i in reader:
        if i[3]==ac_no:
            print('\n\tAccount Name:',i[0])
            print('\tDOB:',i[1])
            print('\tGender:',i[2])
            print('\tAccount No:' ,i[3])
            print('\tAccount Type:',i[4])
            print('\tIFSC:',i[5])
            print('\tPlace:',i[6])
            print('\tPhone no:',i[7])

def billfile(data):
    file=open('Transact.csv','a+',newline='')
    writer=csv.writer(file)
    writer.writerow(data)
    color.write('\tTransaction successful',"STRING")

def bill():#Bill Payments
    print("\n\t\t\t\t\t\tWelcome to Alpha Bank")
    print("\t\t\t\t\t\t\t-Banking at your fingertips")
    color.write("\t\t\t\t\t\tMake Transactions","SYNC")
    print()
    ac_name=input('\tEnter your account name:')
    ac_no=input("\tEnter your account no:")
    typet=input("\tTransaction name:")
    if typet=='Money Deposit':
        amount=int(input("\tType the amount:"))
        data=[ac_name,ac_no,typet,amount,amount]
        billfile(data)
##    elif typet!='Money Deposit':
##        amount=int(input("\tType the amount:"))
##        balance=x-amount
##        billfile([ac_name,ac_no,typet,amount,balance])
        
def transactfile(ac_name):
    file=open('Transact.csv','r')
    reader=csv.reader(file)
    row= file.readlines()[-1].split(',')
    if ac_name==row[0]:
        print('\n\tAccount Name:',row[0])
        print('\tAccount No:',row[1])
        print('\tType:',row[2])
        print('\tAmount:' ,row[3])
        print('\tBalance:',row[4])
            
def transact():
    #Reading from Mysql
    ac_name=input('\tEnter your Account Name:')
    print()
    print('\tPast Transactions:')
    transactfile(ac_name)
        
            
def read(file):#Login page to enter uname and password(Home)
    print("\n\t\t\t\t\t\tWelcome to Alpha Bank")
    print("\t\t\t\t\t\t\t-Banking at your fingertips")
    print()
    color.write("\t\t\t\t\t\tLogin to your account","SYNC")
    reader=csv.reader(file)
    uname=input("\n\tEnter the username:")
    password=input("\tEnter the password:")
    found=False
    for r in reader:
        if (r[0]==uname) and (r[1]==password):
            found=True
    if found==True:
            return cat()
    else:
            color.write("\tIncorrect Username or password!","COMMENT")
            return home()

def home():         # Login page
    file=open('info.csv','a+')
    file.seek(0,0)
    x=read(file)
    file.close()
    return x

start=superhome()
if start==1:
    print(home())
if start==2:
    print(setup())
