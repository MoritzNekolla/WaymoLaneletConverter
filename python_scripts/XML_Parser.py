import math
import os
import uuid
import time

from matplotlib import cm
import matplotlib.animation as animation
import matplotlib.pyplot as plt

import numpy as np
import xml.etree.ElementTree as ET

class XML_Parser(object):

    # data = left_points(x,y), right_points(x,y), velocity
    # return: left_points(x,y, index), right_points(x,yindex), velocity, 
    #              left_way_index, right_way_index, relation_index
    @staticmethod
    def assign_index(data):
        index = 100000
        index_way = 1000
        index_relation = 10
        result = []
        
        for x in range(len(data)):
            single_result = []
            stack = []
            for y in range(len(data[x][0])):
                stack.append(np.concatenate((data[x][0][y], np.array([index]))))
                index = index + 1
            single_result.append(stack)
            stack = []
            for y in range(len(data[x][1])):
                stack.append(np.concatenate((data[x][1][y], np.array([index]))))
                index = index + 1
            single_result.append(stack)
            single_result.append(data[x][2])
            single_result.append(index_way)
            index_way = index_way + 1
            single_result.append(index_way)
            index_way = index_way + 9
            single_result.append(index_relation)
            index_relation = index_relation + 1
            result.append(single_result)
        return result

    
    @staticmethod
    def create_xml(data, path_name):
        usrconfig = ET.Element("usrconfig")
        usrconfig = ET.SubElement(usrconfig,"osm")
        usrconfig.set("version", "0.6")
        usrconfig.set("generator", "JOSM")
        
        for lane in data:
            for lane_L in (lane[0]):
                node = ET.SubElement(usrconfig,"node")
                node.set("id", str(lane_L[2].astype(int)))
                node.set("uid", "1")
                node.set("changeset", "1")
                node.set("version", "1")
                node.set("user ", "1")
                node.set("action", "modify")
                node.set("visible", "true")
                node.set("lat", str(lane_L[0].round(decimals=11)*-1))
                node.set("lon", str(lane_L[1].round(decimals=11)*-1))
            for lane_R in (lane[1]):
                node = ET.SubElement(usrconfig,"node")
                node.set("id", str(lane_R[2].astype(int)))
                node.set("uid", "1")
                node.set("changeset", "1")
                node.set("version", "1")
                node.set("user ", "1")
                node.set("action", "modify")
                node.set("visible", "true")
                node.set("lat", str(lane_R[0].round(decimals=11)*-1))
                node.set("lon", str(lane_R[1].round(decimals=11)*-1))
            
        for lane in data:
            way_L = ET.SubElement(usrconfig,"way")
            way_L.set("id", str(lane[3]))
            way_L.set("action", "modify")
            way_L.set("visible", "true")
            way_L.set("uid", "1")
            way_L.set("changeset", "1")
            way_L.set("version", "1")
            way_L.set("user ", "1")
                
            way_R = ET.SubElement(usrconfig,"way")
            way_R.set("id", str(lane[4]))
            way_R.set("action", "modify")
            way_R.set("visible", "true")
            way_R.set("uid", "1")
            way_R.set("changeset", "1")
            way_R.set("version", "1")
            way_R.set("user ", "1")
            for lane_L in (lane[0]):
                nd_L = ET.SubElement(way_L,"nd")
                nd_L.set("ref", str(lane_L[2].astype(int)))
            for lane_R in (lane[1]):
                nd_R = ET.SubElement(way_R,"nd")
                nd_R.set("ref", str(lane_R[2].astype(int)))
        
        for lane in data:
            relation = ET.SubElement(usrconfig,"relation")
            relation.set("id", str(lane[5]))
            relation.set("action", "modify")
            relation.set("visible", "true")
            relation.set("uid", "1")
            relation.set("changeset", "1")
            relation.set("version", "1")
            relation.set("user ", "1")
            member = ET.SubElement(relation,"member")
            member.set("type", "way")
            member.set("ref", str(lane[3]))
            member.set("role", "left")
            member = ET.SubElement(relation,"member")
            member.set("type", "way")
            member.set("ref", str(lane[4]))
            member.set("role", "right")
            tag = ET.SubElement(relation,"tag")
            tag.set("k", "speedlimit")
            tag.set("v", str(lane[2]))
            tag = ET.SubElement(relation,"tag")
            tag.set("k", "type")
            tag.set("v", "lanelet")
            
            
        tree = ET.ElementTree(usrconfig)         
        tree.write("../data/maps/" + path_name + ".osm",encoding='UTF-8', xml_declaration=True)
        print("Wrote file to: " + path_name + ".osm")

    @staticmethod
    def points_to_xml(data, name):
        data_indexed = XML_Parser.assign_index(data)
        XML_Parser.create_xml(data_indexed, name)