# FIXME: use pecan JSON serialization
def objToDict(obj):
    """
    Convert Entry (or any other object) to dict, because object by default is not JSON serializable, but dict is.
    Instead of changing the business object to match with the requirements of the REST layer,
    the REST layer should make the necessary API <--> business logic transformations.
    (it should be possible to provide different APIs with conflicting requirements for the same business logic)
    :param obj: object to be converted
    :return: dict representation of the data
    """
    if isinstance(obj, object) and hasattr(obj, '__dict__'):
        result = obj.__dict__
    else:
        result = obj

    if isinstance(result, dict):
        result = {key: objToDict(value) for key, value in result.items()}

    if isinstance(result, list):
        result = [objToDict(o) for o in result]

    if isinstance(result, tuple):
        result = tuple(objToDict(o) for o in result)

    return result
