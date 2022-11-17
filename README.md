[![Python 3.8.10](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3810/)

# Totalizador de VVPATs por Visão Computacional

Construção de uma ferramenta para totalização de registros impressos de voto de forma auditável, utilizando visão computacional e primitivas da criptografia (Projeto de Iniciação Científica - DCOMP - UFSJ).

# Requisitos

- [Python](https://python.org) 3.6 ou superior

- Gerenciador de pacotes [_pip_](https://pip.pypa.io/en/stable/installation/)

       python -m ensurepip --upgrade

- Biblioteca [OpenCV](https://opencv.org/)

       pip install opencv-python
       
- Biblioteca [PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/src/introduction.html)
 
       pip install pycryptodomex
       
- Biblioteca [python-barcode](https://python-barcode.readthedocs.io/en/stable/)

       pip install python-barcode
       
- Biblioteca [qrcode](https://pypi.org/project/qrcode/)

       pip install qrcode[pil]
  
- Biblioteca [numpy](https://numpy.org/)

       pip install numpy
    
# Software
- [Visual Studio Code](https://code.visualstudio.com/) (Plugins: Python e Code Runner) 
- [GitHub Desktop](https://desktop.github.com/) (Versionamento Git)

# Módulos Funcionais

- [x] digitalSignature.py
- [x] electionConfiguration.py
- [ ] ellipticCurve.py
- [x] geradorBoletas.py
- [x] geradorVotos.py
- [ ] imprimeResultado.py
- [x] readVote.py
- [x] voteMarking.py
- [ ] voteTotalizationAndVideoRecording.py
- [ ] voteTotalizationByCamera.py
- [ ] voteTotalizationByUrn.py
- [ ] voteTotalizationByVideo.py

# Execução 

### Módulo _electionConfiguration.py_:
      
      python3 electionConfiguration.py
      
- Exemplo de entrada (*):

      Teste
      DCOMP
      3
      01/01/3022
      12:00
      03/01/3022
      12:00
      Cargo 1
      1
      2
      Cargo 2
      2
      1
      Cargo 3
      3
      3
      dcomp
      sjdr

- (*) Devem existir arquivos JSON contendo informações sobre os candidatos e eleitores, assim como as informações dos cargos devem ser compatíveis com os mesmos para que a eleição seja configurada de forma correta.

### Módulo _geradorVotos.py_ (*):
      
      python3 geradorVotos.py
      
- (*) Deve existir uma eleição já cadastrada (por consequência um _layout_ de boleta configurado) para que se possa simular uma escolha de voto isolada.

### Módulo _readVote.py_ (*):
      
      python3 readVote.py
      
- (*) Deve existir previamente uma boleta configurada (e possivelmente com votos marcados) para que esta possa ser lida de forma independente.

# Outros

- [Artigo](https://sol.sbc.org.br/index.php/sbseg_estendido/article/view/21712) curto sobre o projeto, publicado nos Anais Estendidos do Simpósio Brasileiro de Segurança da Informação e de Sistemas Computacionais (SBSeg 2022)
