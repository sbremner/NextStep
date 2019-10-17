def rebuild_cmdline(parts):
    """ VERY naive rebuilding of command line 
        TODO: Update this to be more robust with escaping values.

        Could use shlex.quote but it only works properly for linux CLI
    """
    if not isinstance(parts, (list,tuple)):
        raise ValueError("parts must be a list or tuple")
    
    result = []

    for item in parts:
        # If there is a space, we quote wrap it
        if " " in item:
            result.append('"{}"'.format(item))
        else:
            result.append(item)
    
    return " ".join(result)