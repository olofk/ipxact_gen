#!/usr/bin/env python

import sys
import re

#
# You must include the following class definition at the top of
#   your method specification file.
#
class MethodSpec(object):
    def __init__(self, name='', source='', class_names='',
            class_names_compiled=None):
        """MethodSpec -- A specification of a method.
        Member variables:
            name -- The method name
            source -- The source code for the method.  Must be
                indented to fit in a class definition.
            class_names -- A regular expression that must match the
                class names in which the method is to be inserted.
            class_names_compiled -- The compiled class names.
                generateDS.py will do this compile for you.
        """
        self.name = name
        self.source = source
        if class_names is None:
            self.class_names = ('.*', )
        else:
            self.class_names = class_names
        if class_names_compiled is None:
            self.class_names_compiled = re.compile(self.class_names)
        else:
            self.class_names_compiled = class_names_compiled
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_source(self):
        return self.source
    def set_source(self, source):
        self.source = source
    def get_class_names(self):
        return self.class_names
    def set_class_names(self, class_names):
        self.class_names = class_names
        self.class_names_compiled = re.compile(class_names)
    def get_class_names_compiled(self):
        return self.class_names_compiled
    def set_class_names_compiled(self, class_names_compiled):
        self.class_names_compiled = class_names_compiled
    def match_name(self, class_name):
        """Match against the name of the class currently being generated.
        If this method returns True, the method will be inserted in
          the generated class.
        """
        if self.class_names_compiled.search(class_name):
            return True
        else:
            return False
    def get_interpolated_source(self, values_dict):
        """Get the method source code, interpolating values from values_dict
        into it.  The source returned by this method is inserted into
        the generated class.
        """
        return self.source
    def show(self):
        pass
        #print 'specification:'
        #print '    name: %s' % (self.name, )
        #print self.source
        #print '    class_names: %s' % (self.class_names, )
        #print '    names pat  : %s' % (self.class_names_compiled.pattern, )


#
# Provide one or more method specification such as the following.
# Notes:
# - Each generated class contains a class variable _member_data_items.
#   This variable contains a list of instances of class _MemberSpec.
#   See the definition of class _MemberSpec near the top of the
#   generated superclass file and also section "User Methods" in
#   the documentation, as well as the examples below.

#
# Replace the following method specifications with your own.

#
# Sample method specification #1
#
method1 = MethodSpec(name='walk_and_update',
    source='''\
    def walk_and_update(self):
        members = %(class_name)s._member_data_items
        for member in members:
            obj1 = getattr(self, member.get_name())
            if member.get_data_type() == 'xs:date':
                newvalue = date_calcs.date_from_string(obj1)
                setattr(self, member.get_name(), newvalue)
            elif member.get_container():
                for child in obj1:
                    if type(child) == types.InstanceType:
                        child.walk_and_update()
            else:
                obj1 = getattr(self, member.get_name())
                if type(obj1) == types.InstanceType:
                    obj1.walk_and_update()
        if %(class_name)s.superclass != None:
          %(class_name)s.superclass.walk_and_update(self)
''',
    # class_names=r'^Employee$|^[a-zA-Z]*Dependent$',
    class_names=r'^.*$',
    )


parsex = MethodSpec(name='parsex',
    source='''\
    def parsex(self):
        import re
        expr = self.valueOf_
        base = 10

        horrible_regex_hack = re.compile(r"\('h([0-9A-Fa-f]+)\) / \$pow\(2,(\d+)\) % \$pow\(2,(\d+)\)")
        horrible_regex_match = horrible_regex_hack.match(expr)

        if len(expr) > 2 and expr[0:2] == '0x':
            # handle non-standard SystemVerilog (but commonly-used) syntax
            expr = expr[2:]
            base = 16
        #Super-dirty hack to handle a common pattern used by XSLT upgrade transforms
        elif horrible_regex_match:
            _g = horrible_regex_match.groups()
            expr = str(int(int(_g[0], 16) / 2**int(_g[1]) % 2**int(_g[2])))
            
        elif "'" in expr:
            sep = expr.find("'")
            # ignore any bit size specified before ' because size is handled by other IP-XACT properties
            if expr[sep+1] in ["h", "H"]:
                base = 16
            elif expr[sep+1] in ["d", "D"]:
                base = 10
            elif expr[sep+1] in ["o", "O"]:
                base = 8
            elif expr[sep+1] in ["b", "B"]:
                base = 2
            else:
                raise ValueError("Could not convert expression to an integer: {}".format(self.valueOf_))
            expr = expr[sep+2:]

        return int(expr.replace('_', ''), base)
''',
    class_names=r'^unsignedLongintExpression$|^unsignedIntExpression$|^unsignedPositiveIntExpression$',
    )


#
# Provide a list of your method specifications.
#   This list of specifications must be named METHOD_SPECS.
#
METHOD_SPECS = (
    parsex,
    )
