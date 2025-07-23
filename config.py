# Principais configrações do nosso sistema

DB_PATH = 'dados.db'

# configurações do flask

FLASK_HOST ="127.0.0.1"      # ou 0.0.0.0 para aceitar conexões externas
FLASK_PORT = 5000            # porta de acesso 
FLASK_DEBUG = True           # coloque false para produção
FLASK_THREADED = True        # ativa suporte a multiplos threads
FLASK_USER_RELOADER = True   #atualização automatica ao salvar o arquivo
