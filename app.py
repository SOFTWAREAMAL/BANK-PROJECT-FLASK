from flask import Flask,request,render_template,redirect,url_for
from mysql.connector import * 
mysql=connect(
    host = "localhost",
    user = "root",
    password = "amalan",
    database = "bank")
cursor = mysql.cursor()
create = """
        create table SBI_BANK
        (
        name varchar(50),
        account_no varchar(15),
        password bigint primary key,
        phone_no bigint,
        min_balance int
        );
        """
#cursor.execute(create)
print("success create table")

app=Flask(__name__)

@app.route('/') 
def home_page():
        return render_template('homepage.html')

@app.route('/signin', methods=["POST","GET"])
def signin():
    if request.method == "POST":
        name = request.form.get("name")
        Account_no = request.form.get("account_no")
        phone = request.form.get("phone_no")
        g_mail = request.form.get("g_mail")
        min_balance = request.form.get("min_balance")
        password = request.form.get("password")        
        insert = """
        insert into SBI_BANK(name,account_no,phone_no,g_mail,min_balance,password)
        values(%s,%s,%s,%s,%s,%s);
        """
        i = (name,Account_no,phone,g_mail,min_balance,password)
        cursor.execute(insert,i)
        mysql.commit()
       
        return "<h1> Dear customer your login successful </h1>"
    return render_template('signin.html')

@app.route('/login', methods=["POST","GET"])
def login():
    if request.method == "POST":
        Name=request.form.get("name")
        Password=request.form.get("password")
        cursor.execute('select * from SBI_BANK where name = %s AND password = %s', 
        (Name,Password))
        result=cursor.fetchone()
        print(result)
        if result:
            return f"<h1> Dear customer your login successful {result} </h1>"
        else:
            return "<h1> Invalid </h1>"
    return render_template("login.html")
 
@app.route('/balance', methods=["GET","POST"])
def balance_check():
    if request.method == "POST":
        Account_no  = request.form.get("account_no")
        Password = request.form.get("password")
        cursor.execute('select min_balance from SBI_BANK where Account_no = %s and password = %s ',
        (Account_no,Password))
        result=cursor.fetchone()
        print(result)
        if result:
            return f"<h1> REMAINING BALANCE {result} <h1>"
        else :
            return "<h1> INSUFFICIENT BALANCE</H1>" 
    return render_template('BalanceEnquiry.html')

@app.route('/deposite',methods=["POST","GET"])
def deposite():
    if request.method == "POST":
        Account_no = request.form.get("account_no")
        Password = request.form.get("password")
        amount = request.form.get("amount")
        
        cursor.execute("insert into statement(account_no,password,deposite) values(%s,%s,%s)",(Account_no,Password,amount))
        cursor.execute("update statement set balance = balance + %s where account_no = %s and password = %s",(amount,Account_no,Password))
        
        cursor.execute('update sbi_bank set deposite = %s where account_no = %s and password = %s ',
        (amount,Account_no,Password))
        cursor.execute('update sbi_bank set min_balance = min_balance + deposite where account_no = %s and Password = %s ',
        (Account_no, Password))
        min_balance = cursor.fetchone()
        mysql.commit()
        print(min_balance)
        return "<h1>deposite success !</h1>"
    return render_template('deposite.html')

@app.route('/withdrawal', methods=["POST","GET"])
def withdrawal():
    if request.method == "POST":
        Account_no = request.form.get("account_no")
        Password=request.form.get("password")
        amount = request.form.get("amount")
        
        cursor.execute("insert into statement(account_no,password,withdraw) values(%s,%s,%s)",(Account_no,Password,amount))
        cursor.execute("update statement set balance = balance - %s where balance >=%s and account_no = %s and password = %s",(amount,amount,Account_no,Password))

        cursor.execute('update sbi_bank set withdraw = %s where account_no = %s and password = %s ',
        (amount,Account_no,Password))        
        cursor.execute('select min_balance from sbi_bank where withdraw < min_balance and account_no = %s and password = %s',
        (Account_no, Password))
        min_balance = cursor.fetchone()
        if min_balance :
            cursor.execute('update sbi_bank set min_balance = min_balance - withdraw where account_no = %s and Password = %s ',
            (Account_no, Password))
            mysql.commit()
            print(min_balance)
            return "<h1> withdraw success !</h1>"
        else:
            return "<h1> Insufficient balance ! </h1>"
    return render_template('withdrawal.html')      

@app.route('/ministatement', methods=["POST","GET"])
def ministatement():
    if request.method == "POST":
        Account_no = request.form.get("account_no")
        Password=request.form.get("password")
        cursor.execute('select account_no,deposite,withdraw from statement where account_no = %s and password = %s',(Account_no, Password))
        result = cursor.fetchall()
        mysql.commit()
        if result:
            return render_template('minishow.html',result=result)
    return render_template('mini_statement.html')


@app.route('/logout', methods=["POST","GET"])
def logout():
    if request.method == "POST":
        Name=request.form.get("name")
        Password=request.form.get("password")
        cursor.execute('select * from SBI_BANK where name = %s AND password = %s', 
        (Name,Password))
        result=cursor.fetchone()
        print(result)
        if result:
            return "<h1> Dear customer your logout successful </h1>"
        else:
            return "<h1> Invalid </h1>"
    return render_template("logout.html")

if __name__ == "__main__":
    app.run(debug=True)

cursor.close()
mysql.close()