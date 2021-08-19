import argparse
from os import read, write, chdir, system, popen
from pathlib import Path
from nob import Nob
import sys
import ruamel.yaml
import yaml

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
yaml.indent(mapping=2) # not necessary, this is the default
yaml.preserve_quotes = True


parser = argparse.ArgumentParser(description='Personal information')
parser.add_argument('-f', dest='file_path', type=str, help='file path')

args = parser.parse_args()
imageFile = (args.file_path)


input_file = open(imageFile,"r")
for lines in input_file.read().split():
    line = lines[lines.find("/")+1:]
    chdir("./home_dir")
    stream = open(line+'/values.yaml', 'r')
    data = yaml.load(stream)
    for val in find(data, 'tag'):
      tag = (val)
    chdir("/home/mattan/Desktop/scripts")
    stream = open('values1.yaml', 'r')
    data = yaml.load(stream)
    for val in find(data, 'configmaps'):
      configmaps = (val)

    data = """
      test:
        configmaps: {}
        images:
            tag: {} 
    """.format(configmaps, tag)
    chdir("/home/mattan/Desktop/scripts")
    file = open("hello_cicd_helm_release.yaml","a")
    docs = yaml.load(data)
    yaml.dump(docs, file, transform=PushRootLeft(4))
    file.close()
    


    # dat = str('{{" $imagepolicy": "poc:{}-policy:tag " }}').format(line)
    # dat_braces = f" { dat }"
    # print(dat_braces)

    # chdir("/home/mattan/Desktop/scripts")
    # file = open("hello_cicd_helm_release.yaml","a+")
    # docs = yaml.load(dat_braces,  Loader=yaml.FullLoader)
    # yaml.dump(docs, file)
    # file.close()



data = """
global:
  ingress:
"""
file = open("hello_cicd_helm_release.yaml","a+")
docs = yaml.load(data)
yaml.dump(docs, file, transform=PushRootLeft(4))
file.close()


data = popen("yq e '.common.global.ingress'  values.yaml ").read()
# print (data)
file = open("hello_cicd_helm_release.yaml","a+")
docs = yaml.load(data)
yaml.dump(docs, file, transform=PushRootLeft(8))
file.close()

