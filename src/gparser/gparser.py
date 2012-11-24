'''
Created on Nov 16, 2012

@author: cr
'''
import re


def toJSON(str):
    
    str = str.replace(")]}'\n", "")
    str = str.replace(",,", ",null,")
    str = str.replace(",,", ",null,")
    str = str.replace("[,", "[null,")
    

#    re_object = re.compile(r'{([^"]+):',re.MULTILINE)
#
#    match = re_object.search(str)
#    if match:
#        print match.groups()
        
    #[m.start() for m in re.finditer('{([^"]+):', str)]
    
    
    m = re.search('{([^"]+):', str)
    while m:
#        print m.group()
#        print m.group(1)
        str = str.replace(m.group(), '{"%s":' % m.group(1))
        m = re.search('{([^"]+):', str)
    

    
#    str = str.replace("[[", "{")
#    str = str.replace("]]", "}")



    str = str.replace("[]", "null")
    
    
      
#    str = str.replace("[", "{")
#    str = str.replace("]", "}")

#    str = "[%s}" % str

    return str