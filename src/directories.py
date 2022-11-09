import os

os.chdir('.')
general_data = '/election_data'
stat = '/Static'
logos = '/Logotipos/'
templates = '/Templates/'
componentes = '/Components/'
output = '/Cargas/'
keys = '/Chaves Públicas/'
people = '/JSON/'
boletas = '/Novas Boletas/'
codes = '/Assinaturas/'
bar = '/Barras/'

if not os.path.isdir(os.getcwd() + general_data):
    os.mkdir(os.getcwd() + general_data)
if not os.path.isdir(os.getcwd() + general_data + stat):
    os.mkdir(os.getcwd() + general_data + stat)
if not os.path.isdir(os.getcwd() + general_data + stat + output):
    os.mkdir(os.getcwd() + general_data + stat + output)
if not os.path.isdir(os.getcwd() + general_data + stat + keys):
    os.mkdir(os.getcwd() + general_data + stat + keys)
if not os.path.isdir(os.getcwd() + general_data + stat + logos):
    os.mkdir(os.getcwd() + general_data + stat + logos)
if not os.path.isdir(os.getcwd() + general_data + stat + templates):
    os.mkdir(os.getcwd() + general_data + stat + templates)
if not os.path.isdir(os.getcwd() + general_data + stat + boletas):
    os.mkdir(os.getcwd() + general_data + stat + boletas)
if not os.path.isdir(os.getcwd() + general_data + stat + codes):
    os.mkdir(os.getcwd() + general_data + stat + codes)
if not os.path.isdir(os.getcwd() + general_data + stat + bar):
    os.mkdir(os.getcwd() + general_data + stat + bar)