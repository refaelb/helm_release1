import argparse
from os import read, write, chdir, system, popen
from pathlib import Path
from nob import Nob
import sys
import ruamel.yaml 
import yaml
from ruamel.yaml import YAML  

def find(d, tag):
    if tag in d:
        yield d[tag]
    for k, v in d.items():
        if isinstance(v, dict):
            for i in find(v, tag):
                yield i


class PushRootLeft:
    def __init__(self, positions=42):
        self.positions = positions

    def __call__(self, s):
        result = []
        for line in s.splitlines(True):
            sline = line.strip()
            if not sline or sline[0] == '#':
                result.append(line)
            else:
                result.append(' ' * self.positions + line)
        return ''.join(result)


yaml = ruamel.yaml.YAML()
yaml.indent(mapping=2)
yaml.preserve_quotes = True


parser = argparse.ArgumentParser(description='Personal information')
parser.add_argument('-f', dest='file_path', type=str, help='file path')

args = parser.parse_args()
imageFile = (args.file_path)


data = """
apiVersion: helm.toolkit.fluxcd.io/v2beta1
kind: HelmRelease
metadata:
    name: hello-cicd-test
    namespace: poc
spec:
    interval: 1m
    chart:
        spec:
            chart: hello-cicd-helm
            version: '0.1.0'
            sourceRef:
                kind: HelmRepository
                name: testrepo
                namespace: poc
            interval: 1m
    values:
"""

file = open("hello_cicd_helm_release.yaml","w+")
docs = yaml.load(data)
yaml.dump(docs, file, transform=PushRootLeft(0))
file.close()



input_file = open(imageFile,"r")
for lines in input_file.read().split():
    line = lines[lines.find("/")+1:]
    chdir("home_dir")
    file = open(line+'/values.yaml', 'r')
    data = yaml.load(file)
    for val in find(data, 'tag'):
      tag = (val)
    chdir("../")
    stream = open('configmap.yaml', 'r')
    data = yaml.load(stream)
    for val in find(data, 'configmaps'):
      configmaps = (val)

    dataShit = ''' # {"$imagepolicy": "poc:'''
    dataShitt = '''-policy:tag"}'''
    test = (dataShit + line + dataShitt)
    newstr = test.replace("'", "")
    print(newstr)
    dataTest = """
      test:
        configmaps: {}
        images:
            tag: {}{} """.format(configmaps, tag,newstr)
    file = open("hello_cicd_helm_release.yaml","a")
    docs = yaml.load(dataTest) 
    yaml.dump(docs , file, transform=PushRootLeft(4))


dataGlobal = """
global:
  ingress:
"""
dataIngres = popen("yq e '.common.global.ingress'  ingress.yaml ").read()
file = open("hello_cicd_helm_release.yaml","a+")
docsGlobal = yaml.load(dataGlobal)
docsIngres = yaml.load(dataIngres)
yaml.dump(docsGlobal, file, transform=PushRootLeft(4))
yaml.dump(docsIngres, file, transform=PushRootLeft(8))


