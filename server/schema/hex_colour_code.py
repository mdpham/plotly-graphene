from graphene.types import Scalar
from graphql.language import ast
import json

class HexColour(Scalar):
    # serialize: gets invoked when serializing the result to send it back to a client.
    @staticmethod
    def serialize(col):
        return col
    
    # parseValue: gets invoked to parse client input that was passed through variables.
    @staticmethod
    def parse_literal(node):
        if (isinstance(node, ast.StringValue)):
            return node.value
    # parseLiteral: gets invoked to parse client input that was passed inline in the query.

    @staticmethod
    def hex_to_RGB(hexcode):
        r = int(hexcode[1:3], 16)
        g = int(hexcode[3:5], 16)
        b = int(hexcode[5:7], 16)
        return json.dumps({
            "red": r,
            "green": g,
            "blue": b
        })
    
    @staticmethod
    def RGB_to_hex(r, g, b):
        def reformat(num):
            hexcode = hex(num).upper()
            if (len(hexcode) == 3): # eg. 0xA
                return "0{0}".format(hexcode[-1])
            else: # eg. 0x1A
                return hexcode[-2:] # Last 2 digits
        return "#{0}{1}{2}".format(reformat(r), reformat(g), reformat(b))