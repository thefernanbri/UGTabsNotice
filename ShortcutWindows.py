import os
from win32com.client import Dispatch

# Caminho absoluto do diretório atual
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Caminho do arquivo UGTabsNotice.py (considerando que está na mesma pasta)
arquivo_py = os.path.join(diretorio_atual, "UGTabsNotice.py")

# Caminho para a pasta Startup
pasta_startup = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")

# Caminho para o atalho na pasta Startup
atalho_path = os.path.join(pasta_startup, "UGTabsNotice.lnk")

try:
    # Cria o atalho
    shell = Dispatch("WScript.Shell")
    atalho = shell.CreateShortCut(atalho_path)
    atalho.TargetPath = arquivo_py
    atalho.WorkingDirectory = diretorio_atual
    atalho.Save()
    print("Atalho criado com sucesso!")
except Exception as e:
    print("Ocorreu um erro ao criar o atalho:")
    print(str(e))
