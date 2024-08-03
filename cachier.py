import sqlite3

connection = sqlite3.connect("products.db")
cursor = connection.cursor()

# cursor.execute('''
#         CREATE TABLE IF NOT EXISTS products(
#                id INTEGER PRIMARY KEY,
#                name TEXT NOT NULL,
#                price INTEGER,
#                quantity INTEGER
               
#         )
# ''')

o_username = "admin"
o_password = "admin"

print("Hello on our SUPERMARKET")
print("-"*40)
print("please enter your data to login")
print("-"*40)
username = input("username: ")
password = input("password: ")

#########################################################

def add_products_indb(name, price,quantity):
    cursor.execute('''
                   INSERT INTO products (Name, Price, Quantity)
                   VALUES(? , ? , ?)
                   
                   ''',(name,price,quantity)) 
    
def remove_products_indb(name):
    try:
        cursor.execute('''
                   SELECT * FROM products
                       WHERE name = ?
                   ''',(name,))
        
        product_row = cursor.fetchone()

        if product_row:
            cursor.execute('''
                   DELETE FROM products
                       WHERE name = ?
                   ''',(name,))
            print("The product removed successfully!")
        else:
            print("The product not found!")

    except sqlite3.Error as e:
        print("Error Value: ",e)

def edit_products_indb(name,price,quantity):
    try:
        cursor.execute('''
                   SELECT * FROM products
                       WHERE name = ?
                   ''',(name,))
        
        product_row = cursor.fetchone()

        if product_row:
            cursor.execute('''
                     UPDATE products
                SET Price = ?, Quantity = ?
                WHERE name = ?
                   ''',(price,quantity,name))
            print("The product removed successfully!")
        else:
            print("The product not found!")

    except sqlite3.Error as e:
        print("Error Value: ",e)      

def show_products_indb():
    try:
        cursor.execute('SELECT * FROM products')
        all_rows = cursor.fetchall()

        cursor.execute('PRAGMA table_info(products)')
        column_info = cursor.fetchall()
        column_names = [info[1] for info in column_info]

        if all_rows:
            print(' | '.join(column_names))

            for id, name, price, quantity in all_rows:
                print(f"{id} | {name} | {price} | {quantity}")
        else:
            print("You don't have any products.")

    except sqlite3.Error as e:
        print("Error Value: ", e)  
        
def open_invoice_indb(nams):
    prices = []
    names = nams
    names.pop(-1)
    try:
        for name in names:
            cursor.execute('''
                SELECT * FROM products
                WHERE name = ?
            ''', (name,))

            product_row = cursor.fetchone()

            if product_row:
                cursor.execute('''
                    UPDATE products
                    SET Quantity = Quantity - 1
                    WHERE name = ?
                ''', (name,))

                cursor.execute('SELECT Price FROM products WHERE Name = ?', (name,))
                price = cursor.fetchone()
                prices.append(price[0])
            else:
                if name != 'q':
                    print("The product not found!")

        print('-' * 40)
        print('Your Bill:')
        print(' | '.join(names))
        print(' | '.join(str(price) for price in prices))
        print('Total: ' + str(sum(int(number) for number in prices)) + ' EGP')
        print('-' * 40)

    except sqlite3.Error as e:
        print("Error Value:", e)        
                

                   
####################################################################   

if username == o_username and password == o_password:
    print("-"*40)
    print("welcome to our System")
    print("please choose an option to start")
    print("-"*40)
    print("1. Add product")
    print("2. Delete product")
    print("3. Edit product")
    print("4. Show all products")
    print("5. Open invoice")
    print("6. Exit")
    print("-"*40)

    def add_product():
        print('Please enter the product details:\n')
        name = input('Name: ')
        price = input('Price: ')
        quantity = input('Quantity: ')
        add_products_indb(name, price, quantity)
        print('Product added successfully!')

    def remove_product():
        print('Please enter the name of product you want to remove:\n')
        name = input('Name: ')
        remove_products_indb(name)        

    def edit_product():
        print('Please enter the name of product you want to edit:\n')
        name = input('Name: ')
        print('Please enter the new details:\n')
        price = input('Price: ')
        quantity = input('Quantity: ')
        edit_products_indb(name, price, quantity)

    def show_products():
        print('This is all products:')
        show_products_indb()

    def open_invoice():
        names = []
        while True:
            print('To finish "q"')
            print('Please enter the name of product you want to buy:\n')
            name = input('Name: ')
            names.append(name)
            if name.lower() == 'q':
                open_invoice_indb(names)
                break


   



    option = input('Option: ')
    print('-' * 40)

    if option == '1' or option.lower() == 'add product':
        add_product()

    elif option == '2' or option.lower() == 'remove product':
        remove_product()

    elif option == '3' or option.lower() == 'edit product':
        edit_product()

    elif option == '4' or option.lower() == 'show products':
        show_products()

    elif option == '5' or option.lower() == 'open invoice':
        open_invoice()

    elif option == '6' or option.lower() == 'exit':
        quit()


    else:
        print('Wrong option!')
        quit()


else:
    print('Wrong username or password!')
    quit() 




connection.commit()
connection.close()