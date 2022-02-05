from tabulate import tabulate
import sys


# Define the stuffs that actually matter ;)
mnemonics = ["ACI Data", "ADC A", "ADC B", "ADC C", "ADC D", "ADC E", "ADC H", "ADC L", "ADC M", "ADD A", "ADD B", "ADD C", "ADD D", "ADD E", "ADD H", "ADD L", "ADD M", "ADI Data", "ANA A", "ANA B", "ANA C", "ANA D", "ANA E", "ANA H", "ANA L", "ANA M", "ANI Data", "CALL Label", "CC Label", "CM Label", "CMA", "CMC", "CMP A", "CMP B", "CMP C", "CMP D", "CMP E", "CMP H", "CMP L", "CMP M", "CNC Label", "CNZ Label", "CP Label", "CPE Label", "CPI Data", "CPO Label", "CZ Label", "DAA", "DAD B", "DAD D", "DAD H", "DAD SP", "DCR A", "DCR B", "DCR C", "DCR D", "DCR E", "DCR H", "DCR L", "DCR M", "DCX B", "DCX D", "DCX H", "DCX SP", "DI", "EI", "HLT", "IN Port-Address", "INR A", "INR B", "INR C", "INR D", "INR E", "INR H", "INR L", "INR M", "INX B", "INX D", "INX H", "INX SP", "JC Label", "JM Label", "JMP Label", "JNC Label", "JNZ Label", "JP Label", "JPE Label", "JPO Label", "JZ Label", "LDA Address", "LDAX B", "LDAX D", "LHLD Address", "LXI B, Data", "LXI D, Data", "LXI H, Data", "LXI SP, Data", "MOV A, A", "MOV A, B", "MOV A, C", "MOV A, D", "MOV A, E", "MOV A, H", "MOV A, L", "MOV A, M", "MOV B, A", "MOV B, B", "MOV B, C", "MOV B, D", "MOV B, E", "MOV B, H", "MOV B, L", "MOV B, M", "MOV C, A", "MOV C, B", "MOV C, C", "MOV C, D", "MOV C, E", "MOV C, H", "MOV C, L", "MOV C, M", "MOV D, A", "MOV D, B", "MOV D, C", "MOV D, D", "MOV D, E", "MOV D, H", "MOV D, L", "MOV D, M", "MOV E, A", "MOV E, B", "MOV E, C", "MOV E, D", "MOV E, E", "MOV E, H", "MOV E, L", "MOV E, M", "MOV H, A", "MOV H, B", "MOV H, C", "MOV H, D", "MOV H, E", "MOV H, H", "MOV H, L", "MOV H, M", "MOV L, A", "MOV L, B", "MOV L, C", "MOV L, D", "MOV L, E", "MOV L, H", "MOV L, L", "MOV L, M", "MOV M, A", "MOV M, B", "MOV M, C", "MOV M, D", "MOV M, E", "MOV M, H", "MOV M, L", "MVI A, Data", "MVI B, Data", "MVI C, Data", "MVI D, Data", "MVI E, Data", "MVI H, Data", "MVI L, Data", "MVI M, Data", "NOP", "ORA A", "ORA B", "ORA C", "ORA D", "ORA E", "ORA H", "ORA L", "ORA M", "ORI Data", "OUT Port-Address", "PCHL", "POP B", "POP D", "POP H", "POP PSW", "PUSH B", "PUSH D", "PUSH H", "PUSH PSW", "RAL", "RAR", "RC", "RET", "RIM", "RLC", "RM", "RNC", "RNZ", "RP", "RPE", "RPO", "RRC", "RST 0", "RST 1", "RST 2", "RST 3", "RST 4", "RST 5", "RST 6", "RST 7", "RZ", "SBB A", "SBB B", "SBB C", "SBB D", "SBB E", "SBB H", "SBB L", "SBB M", "SBI Data", "SHLD Address", "SIM", "SPHL", "STA Address", "STAX B", "STAX D", "STC", "SUB A", "SUB B", "SUB C", "SUB D", "SUB E", "SUB H", "SUB L", "SUB M", "SUI Data", "XCHG", "XRA A", "XRA B", "XRA C", "XRA D", "XRA E", "XRA H", "XRA L", "XRA M", "XRI Data", "XTHL"]


opcodes = ["CE", "8F", "88", "89", "8A", "8B", "8C", "8D", "8E", "87", "80", "81", "82", "83", "84", "85", "86", "C6", "A7", "A0", "A1", "A2", "A3", "A4", "A5", "A6", "E6", "CD", "DC", "FC", "2F", "3F", "BF", "B8", "B9", "BA", "BB", "BC", "BD", "BE", "D4", "C4", "F4", "EC", "FE", "E4", "CC", "27", "09", "19", "29", "39", "3D", "05", "0D", "15", "1D", "25", "2D", "35", "0B", "1B", "2B", "3B", "F3", "FB", "76", "DB", "3C", "04", "0C", "14", "1C", "24", "2C", "34", "03", "13", "23", "33", "DA", "FA", "C3", "D2", "C2", "F2", "EA", "E2", "CA", "3A", "0A", "1A", "2A", "01", "11", "21", "31", "7F", "78", "79", "7A", "7B", "7C", "7D", "7E", "47", "40", "41", "42", "43", "44", "45", "46", "4F", "48", "49", "4A", "4B", "4C", "4D", "4E", "57", "50", "51", "52", "53", "54", "55", "56", "5F", "58", "59", "5A", "5B", "5C", "5D", "5E", "67", "60", "61", "62", "63", "64", "65", "66", "6F", "68", "69", "6A", "6B", "6C", "6D", "6E", "77", "70", "71", "72", "73", "74", "75", "3E", "06", "0E", "16", "1E", "26", "2E", "36", "00", "B7", "B0", "B1", "B2", "B3", "B4", "B5", "B6", "F6", "D3", "E9", "C1", "D1", "E1", "F1", "C5", "D5", "E5", "F5", "17", "1F", "D8", "C9", "20", "07", "F8", "D0", "C0", "F0", "E8", "E0", "0F", "C7", "CF", "D7", "DF", "E7", "EF", "F7", "FF", "C8", "9F", "98", "99", "9A", "9B", "9C", "9D", "9E", "DE", "22", "30", "F9", "32", "02", "12", "37", "97", "90", "91", "92", "93", "94", "95", "96", "D6", "EB", "AF", "A8", "A9", "AA", "AB", "AC", "AD", "AE", "EE", "E3"]


bytes_list = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 2, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1]


# Get inputs as arguments from user.
# 1st argument is the filename where the 8085 assembly code is stored
# 2nd argument is the 8085 machine for which addresses are to be generated - either NVIS or Dynalog
argument_list = sys.argv
if(len(argument_list) == 2):
    address = int("2000", base = 16)
elif(argument_list[2].upper() == "NVIS"):
    # Starting address of NVIS kit is 2000H
    address = int("2000", base = 16)
else:
    # Starting address of Dynalog kit is C000H
    address = int("C000", base = 16)


# Open the input csv file
file_input = open(argument_list[1], "r")

# Dictionary to hold label and address pairs
label_dict = {}


# Figure out all the labels and their addresses
for line in file_input:
    # Extract the columns
    columns = line.strip().split(";")

    # If no label is present, move the actual mnemonic to the 2nd index and make the 1st index blank
    if(len(columns) == 1):
        columns.append(columns[0])
        columns[0] = ""

    # If a label is present, add the label and the corresponding address to label_dict
    if(columns[0] != ""):
        label_dict[columns[0]] = hex(address).split("x")[1].upper()
    
    # This would give us all the tuples that start with the string
    for index in range(len(mnemonics)):
        if(mnemonics[index].startswith(columns[1].split(" ")[0])):
            address += bytes_list[index]
            break
    

# Iterate through each line in the input file
file_input.seek(0)
if(len(argument_list) == 2):
    address = int("2000", base = 16)
elif(argument_list[2].upper() == "NVIS"):
    address = int("2000", base = 16)
else:
    address = int("C000", base = 16)

output_columns = [["Address", "Mnemonics", "Opcodes"], ["", "", ""]]

for line in file_input:
    # Ignore blank lines
    if(line.strip() == ""):
        continue

    output_string = ""
    # Extract each column per row
    columns = line.strip().split(";")

    # If no labels are present, move the mnemonic to the 2nd index and make the first index blank
    if(len(columns) == 1):
        columns.append(columns[0])
        columns[0] = ""
    
    # Convert all the stuffs to upper case
    columns[0] = columns[0].upper()
    columns[1] = columns[1].upper()

    # Add the address to the string
    hex_address = hex(address).split("x")[1]
    output_string += hex_address.upper() + "H;"
 

    for index in range(len(mnemonics)):
        if(mnemonics[index].startswith(columns[1].split(" ")[0])):
            # If current mnemonic has a label
            if(mnemonics[index].endswith("Label")):
                for key in label_dict:
                    if(columns[1].endswith(key)):
                        output_string += columns[1].split(" ")[0] + " " + label_dict[key] + "H;"
                        output_string += opcodes[index] + " " + label_dict[key][2:4] + " " + label_dict[key][0:2]
                        address += bytes_list[index]
                        break

            # If current mnemonic has an address
            elif(mnemonics[index].endswith("Address")):
                output_string += columns[1] + ";" + opcodes[index] + " "
                output_string += columns[1].split(" ")[1][2:4] + " " + columns[1].split(" ")[1][0:2]
                address += bytes_list[index]
            
            # If current mnemonic has a data
            elif(mnemonics[index].endswith("Data")):
                mnemonic = columns[1].split(" ")
                if (len(mnemonic) > 2):
                    mnemonic[0] += " " + mnemonic[1]
                for yet_another_index in range(len(mnemonics)):
                    if(mnemonics[yet_another_index].startswith(mnemonic[0])):
                        if(len(mnemonic[len(mnemonic) - 1]) <= 3):
                            output_string += columns[1] + ";" + opcodes[yet_another_index] + " " + mnemonic[len(mnemonic) - 1][0:2]
                        else:
                            output_string += columns[1] + ";" + opcodes[yet_another_index] + " " + mnemonic[len(mnemonic) - 1][2:4]
                            output_string += " " + mnemonic[len(mnemonic) - 1][0:2]
                        address += bytes_list[yet_another_index]
                        break

            else:
                for still_another_index in range(len(mnemonics)):
                    if(mnemonics[still_another_index].startswith(columns[1])):
                        output_string += columns[1] + ";" + opcodes[still_another_index]
                        address += bytes_list[still_another_index]
                        break
            break

    temp_columns = list(output_string.split(";"))
    output_columns.append(temp_columns)

print(tabulate(output_columns))


# Close the files
file_input.close()
