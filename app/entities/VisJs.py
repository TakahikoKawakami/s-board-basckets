import json


class VisJs():
    def __init__(self):
        self.nodeList = []
        self.edgeList = []

    def __str__(self):
        return """
            nodeList: {} counts
            edgeList: {} counts
        """.format(len(self.nodeList), len(self.edgeList))

    def toDict(self):
        result = {
            'nodes': [],
            'edges': []
        }
        for node in self.nodeList:
            result['nodes'].append(node.toDict())
        for edge in self.edgeList:
            result['edges'].append(edge.toDict())

        return result

    class Node():
        def __init__(self, id, label='', uri='', value=1, color="#B69E86"):
            self._id = id
            self._label = label
            self._value = value
            self._uri = uri
            self._color = color
        
        @property
        def id(self):
            return self._id
        @id.setter
        def id(self, value):
            self._id = value
        
        @property
        def label(self):
            return self._label
        @label.setter
        def label(self, value):
            self._label = value
        
        @property
        def uri(self):
            return self._uri
        @uri.setter
        def uri(self, value):
            self._uri = value

        def toDict(self):
            return {
                'id': self._id,
                'label': self._label,
                'value': self._value,
                'uri': self._uri,
                'color': self._color,
            }


    class Edge():
        def __init__(self, fromNode, toNode, width=1, arrows="to"):
            self._from = fromNode
            self._to = toNode
            self._width = width
            # "width": nodeGroup['confidence'],
            self._arrows = "to"

        def toDict(self):
            return {
                'from': self._from,
                'to': self._to,
                'width': self._width,
                'arrows': self._arrows,
            }
