from os import read, write, chdir, system
from pathlib import Path
import yaml
import argparse

parser = argparse.ArgumentParser(description='Personal information')
parser.add_argument('-n', dest='namespace', type=str, help='namespace')
parser.add_argument('-f', dest='file_path', type=str, help='file path')
args = parser.parse_args()
namespace = (args.namespace)
imageFile = (args.file_path)


input_file = open(imageFile,"r")
Path("home_dir").mkdir(parents=True, exist_ok=True)
chdir("./home_dir")
for lines in input_file.read().split():
    line = lines[lines.find("/")+1:] 
    # os.system("helm create "+line )
    Path(line).mkdir(parents=True, exist_ok=True)

    data="""
    replicaCount: 1

    image:
    repository: {}
    pullPolicy: Always
    # Overrides the image tag whose default is the chart appVersion.
    tag: "latest"

    imagePullSecrets: []
    nameOverride: ""
    fullnameOverride: ""

    serviceAccount:
    # Specifies whether a service account should be created
    create: true
    # Annotations to add to the service account
    annotations: {}
    # The name of the service account to use.
    # If not set and create is true, a name is generated using the fullname template
    name: ""

    podAnnotations: {}

    podSecurityContext: {}
    # fsGroup: 2000

    securityContext: {}
    # capabilities:
    #   drop:
    #   - ALL
    # readOnlyRootFilesystem: true
    # runAsNonRoot: true
    # runAsUser: 1000

    service:
    type: ClusterIP
    port: 3000

    ingress:
    enabled: true
    annotations: 
        kubernetes.io/ingress.class: addon-http-application-routing
        # kubernetes.io/ingress.class: nginx
        # kubernetes.io/tls-acme: "true"
    # hosts:
    #     - host: test.ae25bb730d6043dd9638.northeurope.aksapp.io
    #         paths:
    #         - path: /
    #             backend:
    #             serviceName: chart-example.local
    #             servicePort: 3000
    # tls: []
    # #  - secretName: chart-example-tls
    # #    hosts:
    # #      - chart-example.local

    # resources: {}
    # # We usually recommend not to specify default resources and to leave this as a conscious
    # # choice for the user. This also increases chances charts run on environments with little
    # # resources, such as Minikube. If you do want to specify resources, uncomment the following
    # # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
    # # limits:
    # #   cpu: 100m
    # #   memory: 128Mi
    # # requests:
    # #   cpu: 100m
    # #   memory: 128Mi

    # autoscaling:
    # enabled: false
    # minReplicas: 1
    # maxReplicas: 100
    # targetCPUUtilizationPercentage: 80
    # # targetMemoryUtilizationPercentage: 80

    # nodeSelector: {}

    # tolerations: []

    # affinity: {}

    """.format(line,"","","","","","","")
    file = open(line+"/values.yaml","w+")
    docs = yaml.load(data,  Loader=yaml.FullLoader)
    yaml.dump(docs, file)
    file.close()
    
