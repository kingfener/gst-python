# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
#
# gst-python
# Copyright (C) 2002 David I. Lehn
#               2004 Johan Dahlin
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
# 
# Author: David I. Lehn <dlehn@users.sourceforge.net>

from argtypes import UInt64Arg, Int64Arg, PointerArg, ArgMatcher, ArgType, matcher

class GstDataPtrArg(ArgType):
    normal = ('    if (!pygst_data_from_pyobject(py_%(name)s, &%(name)s))\n'
              '        return NULL;\n')
    null =   ('    if (py_%(name)s == Py_None)\n'
              '        %(name)s = NULL;\n'
              '    else if (pyst_data_from_pyobject(py_%(name)s, %(name)s_rect))\n'
              '        %(name)s = &%(name)s_rect;\n'
              '    else\n'
              '            return NULL;\n')
    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pnull:
            info.varlist.add('GstData', pname + '_data')
            info.varlist.add('GstData', '*' + pname)
            info.varlist.add('PyObject', '*py_' + pname + ' = Py_None')
            info.add_parselist('O', ['&py_' + pname], [pname])
            info.arglist.append(pname)
            info.codebefore.append(self.null % {'name':  pname})
        else:
            info.varlist.add('GstData*', pname)
            info.varlist.add('PyObject', '*py_' + pname)
            info.add_parselist('O', ['&py_' + pname], [pname])
            info.arglist.append(pname)
            info.codebefore.append(self.normal % {'name':  pname})

class XmlNodeArg(ArgType):
	"""libxml2 node generator"""
	
	names = {"xobj":"xmlNode",
			"xptr":"xmlNodePtr",
			"xwrap":"libxml_xmlNodePtrWrap"}
	
	parm = ('    if(xml == NULL) return NULL;\n'
			'    xobj = PyObject_GetAttrString(xml, "%(xobj)s");\n'
			'    if(!PyObject_IsInstance(py%(name)s, xobj)) {\n'
			'        PyErr_Clear();\n'
			'        PyErr_SetString(PyExc_RuntimeError,"%(name)s is not a %(xobj)s instance");\n'
			'        Py_DECREF(xobj);Py_DECREF(xml);\n'
			'        return NULL;\n'
			'    }\n'
			'    o = PyObject_GetAttrString(py%(name)s, "_o");\n'
			'    %(name)s = PyCObject_AsVoidPtr(o);\n')
	parmp = ('    Py_DECREF(o); Py_DECREF(xobj);Py_DECREF(xml);\n')
	
	ret =  ('    if(xml == NULL) return NULL;\n')
	retp = ('    xargs = PyTuple_New(1);\n'
			'    xobj = PyObject_GetAttrString(xml, "%(xobj)s");\n'
			'    o = %(xwrap)s(ret);\n'
			'    PyTuple_SetItem(xargs, 0, o);\n'
			'    return PyInstance_New(xobj, xargs, PyDict_New());\n')
	
	def write_param(self, ptype, pname, pdflt, pnull, info):
		info.varlist.add('PyObject', '*xml = _gst_get_libxml2_module()')
		info.varlist.add('PyObject', '*o')
		info.varlist.add('PyObject', '*xobj')
		info.varlist.add('PyObject', '*py' + pname)
		info.varlist.add(self.names["xptr"], pname)
		#if pnull:
		info.add_parselist('O', ['&py'+pname], [pname])
		info.arglist.append(pname)
		self.names["name"] = pname
		info.codebefore.append(self.parm %self.names)
		info.codeafter.append(self.parmp % self.names);
	def write_return(self, ptype, ownsreturn, info):
		info.varlist.add('PyObject', '*xml = _gst_get_libxml2_module()')
		info.varlist.add('PyObject', '*xargs')
		info.varlist.add('PyObject', '*xobj')
		info.varlist.add('PyObject', '*o')
		info.varlist.add(self.names["xptr"], 'ret')
		info.codebefore.append(self.ret % self.names)
		info.codeafter.append(self.retp % self.names)
	
class XmlDocArg(XmlNodeArg):
	"""libxml2 doc generator"""
	names = {"xobj":"xmlDoc",
			"xptr":"xmlDocPtr",
			"xwrap":"libxml_xmlDocPtrWrap"}
			
			
matcher.register('GstData*', GstDataPtrArg())
matcher.register('GstClockTime', UInt64Arg())
matcher.register('GstClockTimeDiff', Int64Arg())
matcher.register('xmlNodePtr', XmlNodeArg())
matcher.register('xmlDocPtr', XmlDocArg())

arg = PointerArg('gpointer', 'G_TYPE_POINTER')
matcher.register('GstClockID', arg)

del arg
