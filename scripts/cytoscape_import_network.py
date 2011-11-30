#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
#       cytoscape_import_network.py
#
#==============================================================================
from optparse import OptionParser
from Tfsuite.Parser.cyto import Cyto
import xmlrpclib
#==============================================================================
#Command line options==========================================================
#==============================================================================
usage = 'usage: %prog [options]'
desc='''%prog takes a network file and loads it into Cytoscape'''
cloptions = OptionParser(usage = usage, description=desc)
cloptions.add_option('-n', '--network', dest = 'net_in',
    help = 'Network input file', metavar='FILE', default = '')
(options, args) = cloptions.parse_args()
#==============================================================================

def connect_server(server_name):
    server = xmlrpclib.ServerProxy(server_name)
    return server



def scale_nodesize(range,id):
    size = 50
    for i in range:
        for node in cytoscape.getNodes():
            connections = len(cytoscape.getNodeNeighbors(id, node))
            if connections >= i:
                cytoscape.setNodeProperty(node,"Node Size", str(size))
        size +=20


def set_color(id):
   for node in cytoscape.getNodes():
        connections= len(cytoscape.getNodeNeighbors(id, node))
        if connections == 1:
            cytoscape.setNodeFillColor(id,[node], 255,0,0)
        elif connections == 2:
            cytoscape.setNodeFillColor(id,[node], 0,255,0)
        elif connections > 2:
            cytoscape.setNodeFillColor(id,[node],0,0,255)

server = connect_server("http://localhost:9000")
cytoscape = server.Cytoscape
title = "bHLH"

if cytoscape.hasCurrentNetwork() == True:
    old_id = cytoscape.getNetworkID()
    cytoscape.destroyNetwork(old_id)
    cytoscape.createNetwork(title)
else:
    cytoscape.createNetwork(title)

network = Cyto()
network.load(options.net_in)
nodes = network.nodes.keys()
from_nodes, to_nodes = network.edges()
cytoscape.createNodes(nodes)
cytoscape.createEdges(from_nodes, to_nodes)
#cytoscape.performDefaultLayout()
cytoscape.performLayout("force-directed")
id = cytoscape.getNetworkID()
scale_nodesize(range(1,50,2),id)
set_color(id)


#cytoscape.setLayoutPropertyValues("kamada-kawai-noweight")
