from django.core.exceptions import ImproperlyConfigured

def get_module_from_module_string(string):
    """
    Given a dot-seperated module string, this method
    imports it then returns the imported Class.
    """
    try:
        import_bits = string[0].rsplit('.', 1)
        module = __import__(import_bits[0], fromlist=[import_bits[1]])
        klass = getattr(module, import_bits[1])
    except ImportError, e:
        raise ImproperlyConfigured("Failed to import %s: %s." % (string, e))
    else:
        return klass
