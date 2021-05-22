print ("loading.")

try:
    import importlib
    importlib.import_module("pyautogui")
except ImportError:
    import pip
    print ("pyautogui not found installing ...")
    pip.main(['install', "pyautogui"])
finally:
    print ("loading....")
    import pyautogui
try:
    importlib.import_module("mysql.connector")
except ImportError:
    import pip
    print("msql connector not found installing ... ")
    pip.main(['install', "MySQL-python"])
finally:
    import mysql.connector
from datetime import datetime
from sys import exit
import  pyautogui


HOST = "localhost"
USER = pyautogui.prompt("Enter Username")
PASSWORD = pyautogui.password("Enter login password") 
DATABASE = "hotel"

def errfound():
    pyautogui.alert("An error has occured due to invalid Params\nPls try again,thank you")
def get_database():
    try:
        database = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        cursor = database.cursor(dictionary=True)
        return database, cursor
    except mysql.connector.Error:
        return None, None


SCREEN_WIDTH = 100


def print_center(s):
    x_pos = SCREEN_WIDTH // 2
    print((" " * x_pos), s)


def print_bar():
    print()

def print_bar_ln():
    print_bar()
    print()


def input_center(s):
    x_pos = SCREEN_WIDTH // 2
    print((" " * x_pos), s, end='')
    return input()


ROOMS_TABLE_NAME = "rooms"


class Room:
    def __init__(self):
        self.room_id = 0
        self.room_no = 0
        self.floor = ""
        self.beds = ""
        self.available = ""

    def create(self, room_id, room_no, floor, beds, available):
        self.room_id = room_id
        self.room_no = room_no
        self.floor = floor
        self.beds = beds
        self.available = available
        return self

    def create_from_record(self, record):
        self.room_id = record['id']
        self.room_no = record['room_no']
        self.floor = record['floor']
        self.beds = record['beds']
        self.available = record['available']
        return self

    def print_all(self):
        a=("Record #"+str( self.room_id))
        b=a+("\nRoom No: "+ str(self.room_no))
        c=b+("\nFloor: "+ str(self.floor))
        d=c+("\nBeds: "+ str(self.beds))
        e=d+("\navailable: "+ str(self.available))
        pyautogui.alert(e)

    def print_full(self):
        a=("Record #"+str( self.room_id))
        b=a+("\nRoom No: "+ str(self.room_no))
        c=b+("\nFloor: "+ str(self.floor))
        d=c+("\nBeds: "+ str(self.beds))
        e=d+("\navailable: "+ str(self.available))
        pyautogui.alert(e)


def create_room():
    room_id = None
    room_no = pyautogui.prompt("Enter the room no: ")
    floor = pyautogui.prompt("Enter the floor (Ex. ground, first etc.): ")
    beds = pyautogui.prompt("Enter number of beds: ")
    available = True
    return Room().create(room_id, room_no, floor, beds, available)


def print_room_header():
    print("="*100)
    print("id".ljust(3),
          "room no".ljust(15),
          "floor".ljust(15),
          "beds".ljust(15),
          "available".ljust(15)
          )
    print("="*100)


def create_rooms_table(database):
    cursor = database.cursor()
    cursor.execute("DROP table if exists {0}".format(ROOMS_TABLE_NAME))
    cursor.execute("create table {0} ("
                   "id int primary key auto_increment,"
                   "room_no int,"
                   "floor varchar(50),"
                   "beds int,"
                   "available bool)".format(ROOMS_TABLE_NAME))


def add_room(database, cursor):
    room = create_room()
    query = "insert into {0}(room_no,floor,beds,available) values({1},'{2}',{3},{4})".\
            format(ROOMS_TABLE_NAME, room.room_no, room.floor, room.beds, room.available)
    try:
        cursor.execute(query)
        database.commit()
    except mysql.connector.Error as err:
        create_rooms_table(database)
        cursor.execute(query)
        database.commit()
    pyautogui.alert("Operation Successful")


def show_room_record(cursor, query):
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        if cursor.rowcount == 0:
            pyautogui.alert("No Matching Records")
            return
        record = records[0]
        room = Room().create_from_record(record)
        room.print_full()
        return room
    except mysql.connector.Error as err:
        print(err)


def show_room_records(cursor, query):
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        if cursor.rowcount == 0:
            pyautogui.alert("No Matching Records")
            return
        print_room_header()
        for record in records:
            room = Room().create_from_record(record)
            room.print_all()
        return records
    except mysql.connector.Error as err:
        print(err)


def get_and_print_room_by_no(cursor):
    room_no = pyautogui.prompt("Enter the room no: ")
    query = "select * from {0} where room_no={1}".format(ROOMS_TABLE_NAME, room_no)
    room = show_room_record(cursor, query)
    return room


def edit_room_by_room_no(database, cursor):
    room = get_and_print_room_by_no(cursor)
    if room is not None:
        query = "update {0} set".format(ROOMS_TABLE_NAME)
        pyautogui.alert("Input new values (leave blank to keep previous value)")
        room_no = pyautogui.prompt("Enter new room no: ")
        if len(room_no) > 0:
            query += " room_no={0},".format(room_no)
        floor = pyautogui.prompt("Enter new floor: ")
        if len(floor) > 0:
            query += " floor='{0}',".format(floor)
        beds = pyautogui.prompt("Enter number of beds: ")
        if len(beds) > 0:
            query += " beds={0},".format(beds)
        query = query[0:-1] + " where id={0}".format(room.room_id)
        confirm = pyautogui.prompt("Confirm Update (Y/N): ").lower()
        if confirm == 'y':
            cursor.execute(query)
            database.commit()
            pyautogui.alert("Operation Successful")
        else:
            pyautogui.alert("Operation Cancelled")


def change_room_status(database, cursor, room_id, available):
    query = "update {0} set available={1} where id={2}".format(ROOMS_TABLE_NAME, available, room_id)
    cursor.execute(query)
    database.commit()


def delete_room_by_room_no(database, cursor):
    room = get_and_print_room_by_no(cursor)
    if room is not None:
        confirm = pyautogui.prompt("Confirm Deletion (Y/N): ").lower()
        if confirm == 'y':
            query = "delete from {0} where id={1}".format(ROOMS_TABLE_NAME, room.room_id)
            cursor.execute(query)
            database.commit()
            pyautogui.alert("Operation Successful")
        else:
            pyautogui.alert("Operation Cancelled")


def room_menu(database, cursor):
    while True:
        choce = (pyautogui.prompt("""
           ROOM MENU
        1. Add new room    
        2. Get room details by room no    
        3. Find available rooms by number of beds
        4. Edit Room details
        5. Delete room
        6. View all rooms
        0. Go Back"""))
        choice=int(choce)

        if choice == 1:
            add_room(database, cursor)
        elif choice == 2:
            room_no = pyautogui.prompt("Enter the room no: ")
            query = "select * from {0} where room_no={1}".format(ROOMS_TABLE_NAME, room_no)
            show_room_records(cursor, query)
        elif choice == 3:
            beds = pyautogui.prompt("Enter number of beds required: ")
            query = "select * from {0} where beds={1}".format(ROOMS_TABLE_NAME, beds)
            show_room_records(cursor, query)
        elif choice == 4:
            edit_room_by_room_no(database, cursor)
        elif choice == 5:
            delete_room_by_room_no(database, cursor)
        elif choice == 6:
            query = "select * from {0}".format(ROOMS_TABLE_NAME)
            show_room_records(cursor, query)
        elif choice == 0:
            break
        else:
            pyautogui.alert("Invalid choice (Press 0 to go back)")


CUSTOMER_TABLE_NAME = "customers"

class Customer:
    def __init__(self):
        self.customer_id = 0
        self.name = ""
        self.address = ""
        self.phone = ""
        self.room_no = "0"
        self.entry_date = ""
        self.checkout_date = ""

    def create(self, customer_id, name, address, phone, room_no, entry_date, checkout_date):
        self.customer_id = customer_id
        self.name = name
        self.address = address
        self.phone = phone
        self.room_no = room_no
        self.entry_date = entry_date
        self.checkout_date = checkout_date
        return self

    def create_from_record(self, record):
        self.customer_id = record['id']
        self.name = record['name']
        self.address = record['address']
        self.phone = record['phone']
        self.room_no = record['room_no']
        self.entry_date = record['entry']
        self.checkout_date = record['checkout']
        return self

    def print_all(self):
        a = ("Patient #"+ str(self.customer_id))
        b = ("Name"+str(self.name))
        c = ("\nAddress: "+ self.address)
        d = ("\nPhone: "+ self.phone)
        e = ("\nChecked in to room #"+ str(self.room_no), " on ", str(self.entry_date.strftime("%d %b %y")))
        f = ("\nCheckout: "+ str(self.checkout_date.strftime("%d %b %y")) if self.checkout_date is not None else None)
        finale=(a+b+c+d+"\n"+str(e)+"\n"+str(f))
        print(finale)
        pyautogui.alert(finale)
    def print_full(self):
        print_bar()
        a = ("Patient #"+ str(self.customer_id))
        b = ("Name"+str(self.name))
        c = ("\nAddress: "+ self.address)
        d = ("\nPhone: "+ self.phone)
        e = ("\nChecked in to room #"+ str(self.room_no), " on ", str(self.entry_date.strftime("%d %b %y")))
        f = ("\nCheckout: "+ str(self.checkout_date.strftime("%d %b %y")) if self.checkout_date is not None else None)
        print_bar()
        pyautogui.alert(a+b+c+d+"\n"+str(e)+"\n"+str(f))


def create_customer(room_no):
    customer_id = None
    name = pyautogui.prompt("Enter the name: ")
    address = pyautogui.prompt("Enter the address: ")
    phone = pyautogui.prompt("Enter the phone: ")
    entry_date = datetime.now()
    return Customer().create(customer_id, name, address, phone, room_no, entry_date, None)


def print_customer_header():
    print("="*100)
    print("id".ljust(3),
          "name".ljust(15),
          "address".ljust(15),
          "phone".ljust(15),
          "room no".ljust(10),
          "entry".ljust(15),
          "check out".ljust(15))
    print("="*100)


def create_customer_table(database):
    cursor = database.cursor()
    cursor.execute("DROP table if exists {0}".format(CUSTOMER_TABLE_NAME))
    cursor.execute("create table {0} ("
                   "id int primary key auto_increment,"
                   "name varchar(20),"
                   "address varchar(50),"
                   "phone varchar(10),"
                   "room_no int,"
                   "entry datetime,"
                   "checkout datetime)".format(CUSTOMER_TABLE_NAME))


NUMBER_OF_RECORDS_PER_PAGE = 10

def add_customer(database, cursor):
    room = get_and_print_room_by_no(cursor)
    if room is not None:
        customer = create_customer(room.room_no)
        confirm = pyautogui.confirm("Confirm checkout? (Y/N): ",buttons=['yes', 'no'])
        if confirm == 'yes':
            query = "insert into {0}(name, address, phone, room_no, entry) values('{1}','{2}','{3}',{4},'{5}')". \
                format(CUSTOMER_TABLE_NAME, customer.name, customer.address, customer.phone,
                       customer.room_no, customer.entry_date.strftime("%Y-%m-%d %H:%M:%S"))
            try:
                cursor.execute(query)
                database.commit()
            except mysql.connector.Error:
                create_customer_table(database)
                cursor.execute(query)
                database.commit()
            change_room_status(database, cursor, room.room_id, False)
            pyautogui.alert("Operation Successful")
        else:
            pyautogui.alert("Operation Canceled")


def show_customer_records(cursor, query):
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        if cursor.rowcount == 0:
            pyautogui.alert("No Matching Records")
            return
        print_customer_header()
        for record in records:
            customer = Customer().create_from_record(record)
            customer.print_all()
        return records
    except mysql.connector.Error as err:
        print(err)


def show_customer_record(cursor, query):
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        if cursor.rowcount == 0:
            pyautogui.alert("No Matching Records")
            return
        record = records[0]
        customer = Customer().create_from_record(record)
        customer.print_full()
        return customer
    except mysql.connector.Error as err:
        print(err)


def get_and_print_customer_by_room_no(cursor):
    room = get_and_print_room_by_no(cursor)
    if room is not None:
        query = "select * from {0} where room_no={1} order by id desc limit 1".format(CUSTOMER_TABLE_NAME, room.room_no)
        customer = show_customer_record(cursor, query)
        return room, customer
    return None, None


def check_out(database, cursor):
    room, customer = get_and_print_customer_by_room_no(cursor)
    if room is not None and customer is not None:
        confirm = pyautogui.confirm("Confirm checkout? (Y/N): ",buttons=['yes', 'no'])
        if confirm == 'yes':
            checkout = datetime.now()
            query = "update {0} set checkout='{1}' where id={2}".\
                format(CUSTOMER_TABLE_NAME, checkout.strftime("%Y-%m-%d %H:%M:%S"), customer.customer_id)
            cursor.execute(query)
            database.commit()
            change_room_status(database, cursor,room.room_id, True)
            pyautogui.alert("Operation Successful")
        else:
            pyautogui.alert("Operation Cancelled")


def edit_customer_by_room_no(database, cursor):
    room, customer = get_and_print_customer_by_room_no(cursor)
    if room is not None and customer is not None:
        query = "update {0} set".format(CUSTOMER_TABLE_NAME)
        pyautogui.alert("Input new values (leave blank to keep previous value)")
        name = pyautogui.prompt("Enter new name: ")
        if len(name) > 0:
            query += " name='{0}',".format(name)
        address = pyautogui.prompt("Enter new address: ")
        if len(address) > 0:
            query += " address='{0}',".format(address)
        phone = pyautogui.prompt("Enter number of phone: ")
        if len(phone) > 0:
            query += " phone='{0}',".format(phone)
        query = query[0:-1] + " where id={0}".format(customer.customer_id)
        confirm =  pyautogui.confirm("Confirm update? (Y/N): ",buttons=['yes', 'no']).lower()
        if confirm == 'yes':
            cursor.execute(query)
            database.commit()
            pyautogui.alert("Operation Successful")
        else:
            pyautogui.alert("Operation Cancelled")


def delete_customer_by_room_no(database, cursor):
    room, customer = get_and_print_customer_by_room_no(cursor)
    if room is not None and customer is not None:
        confirm =  pyautogui.confirm("Confirm update? (Y/N): ",buttons=['yes', 'no']).lower()
        if confirm == 'yes':
            query = "delete from {0} where id={1}".format(CUSTOMER_TABLE_NAME, customer.customer_id)
            cursor.execute(query)
            database.commit()
            pyautogui.alert("Operation Successful")
        else:
            pyautogui.alert("Operation Cancelled")


def customer_menu(database, cursor):
    while True:

        choice = int(pyautogui.prompt("""        
        ==============================
        ==========Patient Menu=========
        ==============================

        ENTER YOUR CHOICE:-
         
        1. New Patient
        2. Show Patient Details by name
        3. Show Patient details by Patient_id
        4. Show Patient details by address
        5. Show Patient details by phone number
        6. Show Patient details by room no
        7. Show Patient details by check in date
        8. Show current list of Patients
        9. Check out
        10. Edit Patient Details
        11. Delete Patient record
        12. View all Patients
        0. Go Back"""))
        if choice == 1:
            add_customer(database, cursor)
        elif choice == 2:
            name = pyautogui.prompt("Enter the name: ").lower()
            query = "select * from {0} where name like '%{1}%'".format(CUSTOMER_TABLE_NAME, name)
            show_customer_records(cursor, query)
        elif choice == 3:
            customer_id = pyautogui.prompt("Enter the Patient id: ")
            query = "select * from {0} where id = {1}".format(CUSTOMER_TABLE_NAME, customer_id)
            show_customer_record(cursor, query)
        elif choice == 4:
            address = pyautogui.prompt("Enter the address: ").lower()
            query = "select * from {0} where address like '%{1}%'".format(CUSTOMER_TABLE_NAME, address)
            show_customer_records(cursor, query)
        elif choice == 5:
            phone = pyautogui.prompt("Enter the phone number: ")
            query = "select * from {0} where phone like '%{1}%'".format(CUSTOMER_TABLE_NAME, phone)
            show_customer_records(cursor, query)
        elif choice == 6:
            room_no = pyautogui.prompt("Enter the room_no: ")
            query = "select * from {0} where room_no = {1}".format(CUSTOMER_TABLE_NAME, room_no)
            show_customer_record(cursor, query)
        elif choice == 7:
            print("Enter the check in date: ")
            day = int(pyautogui.prompt("day of month: "))
            month = int(pyautogui.prompt("month: "))
            year = int(pyautogui.prompt("year: "))
            query = "select * from {0} where date(entry) = '{1}-{2}-{3}'".format(CUSTOMER_TABLE_NAME, year, month, day)
            show_customer_records(cursor, query)
        elif choice == 8:
            query = "select * from {0} where checkout is null".format(CUSTOMER_TABLE_NAME)
            show_customer_records(cursor, query)
        elif choice == 9:
            check_out(database, cursor)
        elif choice == 10:
            edit_customer_by_room_no(database, cursor)
        elif choice == 11:
            delete_customer_by_room_no(database, cursor)
        elif choice == 12:
            query = "select * from {0}".format(CUSTOMER_TABLE_NAME)
            show_customer_records(cursor, query)
        elif choice == 0:
            break
        else:
            pyautogui.alert("Invalid choice (Press 0 to go back)")




if __name__ == '__main__':
    database, cursor = get_database()
    if database is None:
        pyautogui.alert("The Database does not exist or not accessible.")
        exit(1)
    while True:
        
        chice= pyautogui.prompt("""
 HOSPITAL ROOM ALLOTMENT SYSTEM

 
        1. Manage Rooms
        2. Manage Patients
        0. Exit



         Enter your choice: """)
        choice  = int (chice)
        if choice == 1:
            room_menu(database, cursor)
        elif choice == 2:
            customer_menu(database, cursor)
        elif choice == 0:
            break
        else:
            pyautogui.alertInvalid("invaild choice (Press 0 to exit)")
    print_center("GoodBye")
