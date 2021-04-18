from flask import Flask, redirect, url_for, render_template , request

from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='lankster'
app.config['MYSQL_DB']='mobRep'
app.config['MYSQL_CURSORCLASS']= 'DictCursor'

mysql=MySQL(app)

#variables
customer_id=0
estimate='0 Days'
fixable='null'
delete_id=0

customerID=101
customerQuery=''' SELECT firstName,lastName FROM customer WHERE customerID={} '''.format(customerID)

deviceQuery=''' SELECT device.model,device.manufacturer FROM device,customer,gives
    WHERE device.imeiNumber=gives.imeiNumber AND gives.customerID=customer.customerID 
    AND customer.customerID={} '''.format(customerID)

staffQuery=''' SELECT staff.firstName, staff.lastName, staff.staffID FROM staff,fixes,device,gives,customer
    WHERE staff.staffID=fixes.staffID AND fixes.imeiNumber=device.imeiNumber 
    AND device.imeiNumber=gives.imeiNumber AND gives.customerID=customer.customerID 
    AND customer.customerID={} '''.format(customerID)

issueQuery=''' SELECT issue.issueDescription,issue.issueType,issue.fixable,issue.estimatedFixTime FROM issue,device,gives,customer
    WHERE issue.imeiNumber=device.imeiNumber 
    AND device.imeiNumber=gives.imeiNumber AND gives.customerID=customer.customerID 
    AND customer.customerID={} '''.format(customerID)


newFixTime='4 Days'
updateFixTimeQuery=''' UPDATE issue 
    JOIN device ON issue.imeiNumber=device.imeiNumber
    JOIN gives ON device.imeiNumber=gives.imeiNumber
    JOIN customer ON gives.customerID=customer.customerID
    SET issue.estimatedFixTime=%s
    WHERE customer.customerID=%s '''

newFixable='yes'
updateFixableQuery=''' UPDATE issue 
    JOIN device ON issue.imeiNumber=device.imeiNumber
    JOIN gives ON device.imeiNumber=gives.imeiNumber
    JOIN customer ON gives.customerID=customer.customerID
    SET issue.fixable=%s
    WHERE customer.customerID=%s '''

delCustomerID=99
deleteCustomerQuery=''' DELETE FROM Customer WHERE customerID={} '''.format(delete_id)

avgCostQuery=''' SELECT AVG(issue.cost) FROM issue '''

usersPerManufacturerQuery=''' SELECT manufacturer, COUNT(*)
    FROM device,customer,gives
    WHERE device.imeiNumber=gives.imeiNumber AND gives.customerID=customer.customerID
    GROUP BY manufacturer '''


gettingFixedQuery=''' SELECT A.customerID FROM Customer A
    WHERE NOT EXISTS 
        (SELECT D.imeiNumber
        FROM Device D
        WHERE D.imeiNumber NOT IN
            (SELECT E.imeiNumber
            FROM Device E, Fixes F, Staff S
            WHERE E.imeiNumber=F.imeiNumber AND F.staffID=S.staffID AND S.staffID=A.staffID))'''




#get info on a customer
def getCustomerInfo():
    cur=mysql.connection.cursor()
    cur.execute(customerQuery)
    results=cur.fetchall()
    return results

#get info on a customers device
def getDeviceInfo():
    cur=mysql.connection.cursor()
    cur.execute(deviceQuery)
    results=cur.fetchall()
    return results

#get info on the staff member working on a customers device
def getStaffInfo():
    cur=mysql.connection.cursor()
    cur.execute(staffQuery)
    results=cur.fetchall()
    return results

#get info on a customers issue
def getIssueInfo():
    cur=mysql.connection.cursor()
    cur.execute(issueQuery)
    results=cur.fetchall()
    return results

#update the estimated issue fix time for a customer (update + join)
def updateFixTime():
    cur=mysql.connection.cursor()
    cur.execute(updateFixTimeQuery, (estimate,customer_id))
    mysql.connection.commit()

#update wether an issue is fixable or not (update)
def updateFixable():
    cur=mysql.connection.cursor()
    cur.execute(updateFixableQuery, (fixable,customer_id))
    mysql.connection.commit()

#deletes a cusomter query given their customerID (delete + cascade) -maybe show insert to present this
def deleteCustomer():
    cur=mysql.connection.cursor()
    cur.execute(deleteCustomerQuery)
    mysql.connection.commit()

#check the avg. issue cost across all customers (aggregation)
def getAvgCost():
    cur=mysql.connection.cursor()
    cur.execute(avgCostQuery)
    mysql.connection.commit()
    results=cur.fetchall()
    return results

#get the number of customer with a device from each manufacturer (aggregation + group-by)
def getUsersPerManufacturer():
    cur=mysql.connection.cursor()
    cur.execute(usersPerManufacturerQuery)
    mysql.connection.commit()
    results=cur.fetchall()
    return results

#find all the customers that their device is getting fixed (divison: NOT EXISTS - NOT IN query)
def getGettingFixed():
    cur=mysql.connection.cursor()
    cur.execute(gettingFixedQuery)
    mysql.connection.commit()
    results=cur.fetchall()
    return results


@app.route("/")
def home():
    customerKeys = (
        
        "firstName",
        "lastName",
        "address",
        "email",
        "phone",
        "staffID",
        
        "ReferenceNumber",
        
    )
    customerValues = (
    
        "brad",
        "bak",
        "203 north rd",
        "brad@gmail.com",
        "778-222-8497",
        1,
        
        "100",
        
    )
    customer = [
        (customerKeys[i], customerValues[i]) for i, _ in enumerate(customerKeys)
    ]
    return render_template("status.html", customer=customer, steps=[1, 1, 1, 0])

@app.route("/update",methods = ['POST', 'GET'])
def shop_update():
    global customer_id 
    global estimate 
    global fixable 
    global delete_id

    if request.method == 'POST':
        customer_id = request.form['id']
        estimate = request.form['fixtime']
        fixable = request.form['fixable']
        delete_id=request.form['del-id']
        #print(customer_id)
        #print(estimate)
        #print(fixable)
        #print(delete_id)
        updateFixTime()
        updateFixable()
        deleteCustomer()

        #avg cost of device
        avgCost=getAvgCost()
        print(avgCost)

        #number of users with devices for each different manufacturer
        usersPerManufacturer=getUsersPerManufacturer()
        print(usersPerManufacturer)

        return render_template("update.html") 

    else:
        customer_id = request.args.get('id')
        customer_id = request.args.get('fixtime')
        customer_id = request.args.get('fixable')
        customer_id = request.args.get('del-id')
        return render_template("update.html")
  







@app.route("/contact")
def test():
    return render_template("contact.html")


@app.route("/contact/post")
def contact_post():
    return


if __name__ == "__main__":
    app.run(debug=True)
