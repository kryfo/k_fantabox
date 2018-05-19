import sys
import os
import hashlib

def md5sum(fname): 
    def read_chunks(fh): 
        fh.seek(0) 
        chunk = fh.read(8096) 
        while chunk: 
            yield chunk 
            chunk = fh.read(8096) 
        else: 
            fh.seek(0) 
    m = hashlib.md5() 
    if isinstance(fname, basestring) and os.path.exists(fname): 
        with open(fname, "rb") as fh: 
            for chunk in read_chunks(fh): 
                m.update(chunk) 

    elif fname.__class__.__name__ in ["StringIO", "StringO"] or isinstance(fname, file): 
        for chunk in read_chunks(fname): 
            m.update(chunk) 
    else: 
        return "" 
    return m.hexdigest()