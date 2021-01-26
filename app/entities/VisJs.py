class VisJs():
    def __init__(self):
        self.nodeList = []
        self.edgeList = []

    class Node():
        def __init__(self, id, label, uri, value=1, color="#B69E86"):
            self._id = id
            self._label = label
            self._value = value
            self._uri = uri
            self._color = color


    class Edge():
        def __init__(self, fromNode, toNode, width, arrows="to"):
            self._from = fromNode
            self._to = toNode
            self._width = width
            # "width": nodeGroup['confidence'],
            self._arrows = "to"