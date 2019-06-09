import mysql.connector
from mysql.connector import Error


def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def insertBLOB(photo):
    print("Inserting BLOB into python_employee table")
    try:
        connection = mysql.connector.connect(host='3.16.229.70',
                             database='lifesports',
                             user='root',
                             password='1111')
        
        if connection.is_connected() :
                cursor = connection.cursor()

                sql_insert_blob_query = """ INSERT INTO gym
                                (gym_fig) VALUES (%s,)"""
                empPicture = convertToBinaryData(photo)
                # Convert data into tuple format
                insert_blob_tuple = (empPicture)

                result  = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
                connection.commit()
                print ("Image and file inserted successfully as a BLOB into python_employee table", result)
    except mysql.connector.Error as error :
        connection.rollback()
        print("Failed inserting BLOB data into MySQL table {}".format(error))
    finally:
        #closing database connection.
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


insertBLOB("photo.jpeg")
