#Embed the API summary in comments. The overview is in line with MSDN.
#@author Bigdrea6
#@category Windows Analysis

import json

api_summary = {}

def set_summary(api, addr):
    if api not in api_summary.keys():
        print("[!] Not support {}".format(api))
    else:
        if getEOLComment(addr) != api_summary[api]:
            setEOLComment(addr, api_summary[api])

def make_table():
    for externalReference in currentProgram.getReferenceManager().getExternalReferences():
        if externalReference.getReferenceType().isCall():
            call_addr = externalReference.getFromAddress()
            api = externalReference.getExternalLocation().getLabel()

            if api[-1] == 'A' or api[-1] == 'W':
                api = api[:-1]
            
            set_summary(api, call_addr)

def load_dict():
    global api_summary
    try:
        dataset = askFile("Choose dataset:", "Set").toString()
        with open(dataset, 'r') as f:
            api_summary = json.load(f)
        print("[+]Loaded File")
    except ghidra.util.exception.CancelledException:
        print("[!]Cancelled")

if __name__ == '__main__':
    load_dict()
    make_table()