

#######################################################################################################################

def is_numeric(a):
    
    """
    Check if parameter a can be converted to int
    """
    try:
        int(a)
        return True
    except:
        return False
