import cx_Oracle
from tabulate import tabulate
import sys

# Setup the connection
connection = cx_Oracle.connect("SYSTEM/password")
# Get a cursor object
cursor = connection.cursor()


argument_list = sys.argv
if(argument_list[2] == "NVIS"):
    # Starting address of NVIS kit is 2000H
    address = int("2000", base = 16)
else:
    # Starting address of Dynalog kit is C000H
    address = int("C000", base = 16)


# Open the input csv file

# file_input = open("Table_CSV_Convert.csv", "r")
file_input = open(argument_list[1], "r")
# Open the output csv file
#file_output = open("Table_CSV_Convert_Output.csv", "w")

# Dictionary to hold label and address pairs
label_dict = {}



# Figure out all the labels and their addresses
for line in file_input:
    # Extract the columns
    columns = line.strip().split(";")

    # If a label is present, add the label and the corresponding address to label_dict
    if(columns[0] != ""):
        label_dict[columns[0]] = hex(address).split("x")[1].upper()
    
    # This would give us all the tuples that start with the string
    cursor.execute("SELECT * FROM Opcodes8085 WHERE Mnemonics LIKE '" + columns[1].split(" ")[0] + "%'")
    for tuple in cursor:
        address += tuple[2]
        # Although we get a lot of similar tuples, we need only the 1st one.
        # So we break in the 1st iteration
        break
    



# Iterate through each line in the input file
file_input.seek(0)
if(argument_list[2] == "NVIS"):
    address = int("2000", base = 16)
else:
    address = int("C000", base = 16)
output_columns = [["Address", "Mnemonics", "Opcodes"], ["", "", ""]]
for line in file_input:
    output_string = ""
    # Extract each column per row
    columns = line.strip().split(";")

    # Add the address to the string
    hex_address = hex(address).split("x")[1]
    output_string += hex_address.upper() + "H;"
 

    cursor.execute("SELECT * FROM Opcodes8085 WHERE Mnemonics LIKE '" + columns[1].split(" ")[0] + "%'")
    for tuple in cursor:
        # If current mnemonic has a label
        if(tuple[0].endswith("Label")):
            for key in label_dict:
                if(columns[1].endswith(key)):
                    output_string += columns[1].split(" ")[0] + " " + label_dict[key] + "H;"
                    output_string += tuple[1] + " " + label_dict[key][2:4] + " " + label_dict[key][0:2]
                    address += tuple[2]
                    break

        # If current mnemonic has an address
        elif(tuple[0].endswith("Address")):
            output_string += columns[1] + ";" + tuple[1] + " "
            output_string += columns[1].split(" ")[1][2:4] + " " + columns[1].split(" ")[1][0:2]
            address += tuple[2]
        
        # If current mnemonic has a data
        elif(tuple[0].endswith("Data")):
            mnemonic = columns[1].split(" ")
            if (len(mnemonic) > 2):
                mnemonic[0] += " " + mnemonic[1]
            cursor.execute("SELECT * FROM Opcodes8085 WHERE Mnemonics LIKE '" + mnemonic[0] + "%'")
            for tuple2 in cursor:
                if(len(mnemonic[len(mnemonic) - 1]) <= 3):
                    output_string += columns[1] + ";" + tuple2[1] + " " + mnemonic[len(mnemonic) - 1][0:2]
                else:
                    output_string += columns[1] + ";" + tuple2[1] + " " + mnemonic[len(mnemonic) - 1][2:4]
                    output_string += " " + mnemonic[len(mnemonic) - 1][0:2]
                address += tuple2[2]
                break

        else:
            cursor.execute("SELECT * FROM Opcodes8085 WHERE Mnemonics = '" + columns[1] + "'")
            for tuple2 in cursor:
                output_string += columns[1] + ";" + tuple2[1]
                address += tuple2[2]
                break
        break

    temp_columns = list(output_string.split(";"))
    output_columns.append(temp_columns)

    #file_output.write(output_string + "\n")

print(tabulate(output_columns))



# Close the files
file_input.close()
#file_output.close()
# Close the connection
connection.close()
