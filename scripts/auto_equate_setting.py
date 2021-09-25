#The equation is set automatically. 
#However, only four APIs are supported: SHGetSpecialFolderPathA, RegCreateKeyExA, RegSetValueExA, and CreateProcessA.
#This is a prototype. I plan to develop it.
#@author Bigdrea6
#@category Windows Analysis(prototype)

from ghidra.app.decompiler import DecompInterface
from ghidra.program.model.pcode import PcodeOp, DynamicHash
from ghidra.program.model.symbol.Equate import addReference
import json

decompiler = DecompInterface()
decompiler.openProgram(currentProgram)

api_dict = {}
created_eq = {}

def set_equate(vnode, equate):
    global created_eq
    if equate in created_eq:
        new_eq = created_eq[equate]
    else:
        new_eq = currentProgram.getEquateTable().createEquate(equate, vnode.getOffset())
        created_eq[equate] = new_eq

    dynamic_hash = DynamicHash(vnode, 0)
    new_eq.addReference(dynamic_hash.getHash(), dynamic_hash.getAddress())

def confirm_argument(addr, api):
    constant_subscripts = []
    equates = []

    func = getFunctionContaining(addr)
    hfunc = decompiler.decompileFunction(func, 0, None).getHighFunction()

    for hpcode in hfunc.getPcodeOps(addr):
        if hpcode.getOpcode() == PcodeOp.CALL:
            target_subscripts = api_dict[api]['target_subscript']

            for subscript in target_subscripts:
                vnode = hpcode.getInput(subscript)

                if vnode.isConstant():
                    constant_subscripts.append(subscript)

                    if subscript in api_dict[api]['verifi_offset']:
                        offset = vnode.getOffset()
                        equate = api_dict[api][str(subscript)][str(offset)]
                        equates.append(equate)

                        set_equate(vnode, equate)
                    else:
                        equate = api_dict[api][str(subscript)]
                        equates.append(equate)

                        set_equate(vnode, equate)

    print("[+]{} {} {}".format(api, constant_subscripts, equates))

def make_table():
    for externalReference in currentProgram.getReferenceManager().getExternalReferences():
        if externalReference.getReferenceType().isCall():
            call_addr = externalReference.getFromAddress()
            api = externalReference.getExternalLocation().getLabel()
            
            if api in api_dict:
                confirm_argument(call_addr, api)

def load_dict():
    global api_dict
    try:
        dataset = askFile("Choose dataset:", "Equate Table").toString()
        with open(dataset, 'r') as f:
            api_dict = json.load(f)
        print("[+]Loaded File")
    except ghidra.util.exception.CancelledException:
        print("[!]Cancelled")

if __name__ == '__main__':
    load_dict()
    make_table()