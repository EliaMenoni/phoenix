from typing import Any, List, Dict
from xml.etree import ElementTree as et
from . import models
def get_members(obj: object) -> List[str]:
    """ Helper function
        Get class members other than functions and private members.
    """
    members = []
    for attr in dir(obj):
        if not callable(getattr(obj, attr)) and not attr.startswith("__"):
            members.append(attr)
    return members

def to_xml(obj: Any) -> Any:
    """ Convert a class object and its members to XML.

    Each class member is treated as a tag to the current XML-element.
    Each member object is treated as a new sub-element.
    Each 'list' member is treated as a new list tag.
    """

    if isinstance(obj, dict):
        raise Exception("Dictionary type is not supported.")

    root = None
    tags = {}

    subelements = {}  # type: Dict[Any, Any]
    for member in get_members(obj):
        item = getattr(obj, member)
        if(member == "_NAME" or member == "_TEXT"):
            continue
        # member = member.replace('_', '-')

        # if object is None, add empty tag
        if item is not None:
            # Add list sub-elements
            if isinstance(item, (list, set, tuple)):
                subelements[member] = []
                for list_object in item:
                    subelements[member].append(to_xml(list_object))
            # Add sub-element
            elif not isinstance(item, (str, list, set, tuple)):
                subelements[member] = to_xml(item)
            # Add element's tag name
            else:
                tags[member] = item

    try:
        if obj._NAME:
            root = et.Element(obj._NAME, tags)
        else:
            raise Exception("Name attribute can't be empty.")
    except (AttributeError, TypeError) as ex:
        print("Attribute value or type is wrong. %s: %s", obj, ex)
        raise

    # Add sub elements if any
    if subelements:
        for name, values in subelements.items():
            if isinstance(values, list):  # if list of elements. Add all sub-elements
                sub = et.SubElement(root, name)
                for value in values:
                    sub.append(value)
            else:  # single sub-child or None
                if values is None:  # if None, add empty tag with name
                    sub = et.SubElement(root, name)
                else:  # else add object
                    root.append(values)

    try:
        if obj._TEXT:
            root.text = obj._TEXT
    except AttributeError as ex:
        print("Attribute does not exists. %s: %s", obj, ex)
        raise

    return root

def object_to_xml(obj: Any) -> Any:
    """ Convert the given class object to xml document str.
    """
    return et.tostring(element=to_xml(obj), encoding="UTF-8")

def compose_LDO(json_data):
    HEADER = models.LDO_HEADER(json_data.get("header"))
    # BODY = models.LDO_HEADER(json_data.get("body"))

    return HEADER
