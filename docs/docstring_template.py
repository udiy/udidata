def docstring_template(desc, params, returns):
    """
    Returns a string at a specific formating for a docstring

    Parameters
    ----------
    desc : str
        A short description at the top of the docstring
    params : dict
        A dictionary of parameters and string description
    returns : str
        A short description of expected object to return

    Returns
    -------
    docstring : str
    """

    docstring = f"""
    {desc}

    Parameters
    ----------
    {params}

    Returns
    -------
    {returns}
    """

    return docstring