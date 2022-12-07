import os

current_dir = os.getcwd()
general_data = '/election_data'
stat = '/Static'
logos = '/Logotipos/'
templates = '/Templates/'
componentes = '/Components/'
output = '/Cargas/'
fingerprints = '/Fingerprints/'
keys = '/Chaves Públicas/'
people = '/JSON/'
boletas = '/Novas Boletas/'
codes = '/Assinaturas/'
bar = '/Barras/'
ver = '/v1.0/'
videos = 'Vídeos/'

if not os.path.isdir(current_dir + general_data):
    os.mkdir(current_dir + general_data)
if not os.path.isdir(os.getcwd() + general_data + ver):
    os.mkdir(os.getcwd() + general_data + ver)
if not os.path.isdir(os.getcwd() + general_data + ver + videos):
    os.mkdir(os.getcwd() + general_data + ver + videos)
if not os.path.isdir(current_dir + general_data + stat):
    os.mkdir(current_dir + general_data + stat)
if not os.path.isdir(current_dir + general_data + stat + output):
    os.mkdir(current_dir + general_data + stat + output)
if not os.path.isdir(current_dir + general_data + stat + fingerprints):
    os.mkdir(current_dir + general_data + stat + fingerprints)
if not os.path.isdir(current_dir + general_data + stat + keys):
    os.mkdir(current_dir + general_data + stat + keys)
if not os.path.isdir(current_dir + general_data + stat + logos):
    os.mkdir(current_dir + general_data + stat + logos)
if not os.path.isdir(current_dir + general_data + stat + templates):
    os.mkdir(current_dir + general_data + stat + templates)
if not os.path.isdir(current_dir + general_data + stat + boletas):
    os.mkdir(current_dir + general_data + stat + boletas)
if not os.path.isdir(current_dir + general_data + stat + codes):
    os.mkdir(current_dir + general_data + stat + codes)
if not os.path.isdir(current_dir + general_data + stat + bar):
    os.mkdir(current_dir + general_data + stat + bar)