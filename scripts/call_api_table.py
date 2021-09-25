#Create a table of Windows APIs and the addresses to CALL them.
#@author Bigdrea6
#@category Windows Analysis

from collections import Counter

table = []
table2 = []

for externalReference in currentProgram.getReferenceManager().getExternalReferences():
    if externalReference.getReferenceType().isCall():
        call_addr = externalReference.getFromAddress()
        api = externalReference.getExternalLocation().getLabel()

        set = []
        set.extend([call_addr, api])
        table.append(set)
        table2.append(api)

table = sorted(table)

for i in range(len(table)):
    print("{} : {}".format(table[i][0], table[i][1]))

print("API Types:{}, Call Count:{}".format(len(Counter(table2)), len(table)))