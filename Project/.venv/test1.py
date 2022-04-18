import sqlite3
con = sqlite3.connect("PMA")
print("Enter Fname:")
Fname = input()

print("Enter Lname:")
Lname = input()
print("Enter password:")
password = input()

print("Confirm password:")
Cpassword = input()

query = "insert into signup(Fname, Lname, Password, Cpassword) values('"+Fname+"','"+Lname+"','"+password+"','"+Cpassword+"')"
con.execute(query)
con.commit()
con.close()

print("Data saved...")