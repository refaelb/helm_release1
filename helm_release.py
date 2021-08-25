import argparse
from os import read, write, chdir, system, popen
from pathlib import Path
from nob import Nob
import sys
import ruamel.yaml 
import yaml
from ruamel.yaml import YAML  
from pushRootLeft import PushRootLeft

data1 = """
apiVersion: helm.toolkit.fluxcd.io/v2beta1
kind: HelmRelease
metadata:
    name: {}
    namespace: {}
spec:
    interval: 1m
    chart:
        spec:
            chart: {}
            version: '0.1.0'
            sourceRef:
                kind: HelmRepository
                name: {}
                namespace: {}
            interval: 1m
    values:
"""
data2 = ''' # {"$imagepolicy": "poc:'''
data3 = '''-policy:tag"}'''
data4 = """
{}:
images:
    tag: {}{} """
data5 = """
global:
  ingress:
"""
data6 = popen("yq e '.common.global.ingress'  umbrella/{}/values.yaml ")


### Searches within a file for the value ###
def find(File, value):
    if value in File:
        yield File[value]
    for k, v in File.items():
        if isinstance(v, dict):
            for i in find(v, value):
                yield i


yaml = ruamel.yaml.YAML()
yaml.indent(mapping=2)
yaml.preserve_quotes = True

parser = argparse.ArgumentParser(description='Personal information')
parser.add_argument('-f', dest='file_path', type=str, help='file path')
parser.add_argument('-name', dest='name', type=str, help='name')
parser.add_argument('-r', dest='repository', type=str, help='repository')
parser.add_argument('-n', dest='namespace', type=str, help='namespace')
parser.add_argument('-c', dest='chart_name', type=str, help='chart name')
parser.add_argument('-father-chart', dest='father_chart', type=str, help='father chart')

args = parser.parse_args()
imageFile = (args.file_path)
nameSpace = (args.namespace)
chartName = (args.chart_name)
repository = (args.repository)
name = (args.name)
father_chart = (args.father_chart)

file = open("{}.yaml".format(name),"w+")
docs = yaml.load(data1.format(name,nameSpace,chartName,repository,nameSpace))
yaml.dump(docs, file)
file.close()

input_file = open(imageFile,"r")
for lines in input_file.read().split():
    line = lines[lines.find("/")+1:]
    chdir("umbrella")
    file = open(line+'/values.yaml', 'r')
    data = yaml.load(file)
    for val in find(data, 'tag'):
      tag = (val)
    chdir("../")
    shit = (data2 + line + data3)
    newstr = shit.replace("'", "")
    
    file = open("{}.yaml".format(name),"a")
    docs = yaml.load(data4.format(line, tag,newstr)) 
    yaml.dump(docs , file, transform=PushRootLeft(4))

file = open("{}.yaml".format(name),"a+")
docsGlobal = yaml.load(data5)
docsIngres = yaml.load(data6.format(father_chart)).read()
yaml.dump(docsGlobal, file, transform=PushRootLeft(4))
yaml.dump(docsIngres, file, transform=PushRootLeft(8))


