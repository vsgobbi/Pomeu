#!/usr/bin/env python2
# Modified Vitor Sgobbi, 2014
# ICEA (Air traffic control insitute) - Brazil
# This code is licensed GPL

import sys
import signal
import gobject
import os.path
import os
import subprocess
#import psutils
from optparse import OptionParser
try:
    	import yaml
except:
    	print "YAML is not supported. options.yaml will not function"
    	print "Arquivo OPTIONS.YAML nao econtrado, mudar os diretorios..."

#PERCENT_MATCH_LIMIT = 75 #filtro a ser implementado para futura versao

# Buscar arquivos, where are the files?
# se houver erro ao encontrar arquivos, setar os parametros
conf_dir = os.path.dirname(os.path.realpath(__file__)) #diretorio do arq executado no terminal
lang_dir = os.path.join(conf_dir, "language")
command_file = os.path.join(conf_dir, "commands.conf")
strings_file = os.path.join(conf_dir, "sentences.corpus")
history_file = os.path.join(conf_dir, "arqHist.history")
opt_file = os.path.join(conf_dir, "options.yaml")
lang_file = os.path.join(lang_dir, 'lm')
dic_file = os.path.join(lang_dir, 'dic')
#cria diretorio language se arquivos n existirem
#make the lang_dir if it doesn't exist
if not os.path.exists(lang_dir):
        os.makedirs(lang_dir)

#filtro a ser adicionado para aumentar a precisao de matching...
#if biggestKeyCount > 0 and ((len(textWords) <= 2 and len(biggestKeySet)) == len(textWords)) or percentMatch >= PERCENT_MATCH_LIMIT):
    #print ("Melhor combinacao: " + biggestKey, "Detectado: " + text.lower(), "Porcentagem de combinacao: " + str(percentMatch));
    #cmd = self.commands[biggestKey]

class Pomeu:
    def __init__(self, opts):
        #importar recognizer:
        from Recognizer import Recognizer
        self.ui = None
        self.options = {}
        ui_continuous_listen = False
        self.continuous_listen = False
        self.commands = {}
        self.read_commands()
        self.recognizer = Recognizer(lang_file, dic_file, opts.microphone)
        self.recognizer.connect('finished', self.recognizer_finished)

        #abrir o arquivo de opcoes
        self.load_options()
        #merge the opts
        for k, v in opts.__dict__.items():
            if not k in self.options:
                self.options[k] = v

        print "Opcoes de uso: ", self.options

        if self.options['interface'] != None:
            if self.options['interface'] == "qt":
                from QtUI import UI
            elif self.options['interface'] == "g":
                from GtkUI import UI
            elif self.options['interface'] == "gt":
            	from GtkTrayUI import UI
            else:
                print "nenhuma GUI definida"
                sys.exit()
            self.ui = UI(args, self.options['continuous'])
            self.ui.connect("command", self.process_command)
                #arquivo de icone principal
            icon = self.load_resource("icon.png")
            if icon:
                self.ui.set_icon_active_asset(icon)


                #icone quando inativo
                icon_inactive = self.load_resource("icon_inactive.png")
                if icon_inactive:
                    self.ui.set_icon_inactive_asset(icon_inactive)

            if self.options['history']:
                self.history = []


    def read_commands(self):
        #le o arquivo de commandos commands.conf
        file_lines = open(command_file)
        strings = open(strings_file, "w")
        for line in file_lines:
                print line
                #cortar os espacos em branco
                line = line.strip()
                #se a linha n tiver o primeiro char com hash # = comentario
                if len(line) and line[0] != "#":
                                #linha de parsing
                                (key, value) = line.split(":", 1)
                                print key, value
                                self.commands[key.strip().lower()] = value.strip()
                                strings.write(key.strip()+"\n")
        #close the strings file
        strings.close()


    #abrir o arquivo de opcoes .yaml
    def load_options(self):
        try:
            opt_fh = open(opt_file)
            text = opt_fh.read()
            self.options = yaml.load(text)
        except:
            pass


    #armazenar historico e retirar primeiro item
    def log_history(self, text):
        if self.options['history']:
            self.history.append(text)
            if len(self.history) > self.options['history']:
                #primeiro item da "pilha"
                self.history.pop(0)

            #abrir e truncar arqvo de hist
            hfile = open(history_file, "w")
            for line in self.history:
                hfile.write(line + "\n")
            #fechar arqvo de hist
            hfile.close()


    #printar se comando encontrado
    def recognizer_finished(self, recognizer, text):
        t = text.lower()  #setando para lower case???
        #existe algum comando encontrado?
        if self.commands.has_key(t):
            cmd = self.commands[t]
            print cmd
            subprocess.call(cmd, shell=True)
            self.log_history(text)  #armazena hist
        else:
            print "Comando nao econtrado, fale novamente..."
        #se nao for modo de escuta continuo na interface grafica
        if self.ui:
            if not self.continuous_listen:
                #pausar
                self.recognizer.pause()
            #finalizar comando t, t(erminal)
            self.ui.finished(t)


    #executa app
    def run(self):
        if self.ui:
            self.ui.run()
        else:
            pomeu.recognizer.listen()

    #melhorar sign de saida
    def quit(self):
        sys.exit()


    def process_command(self, UI, command):
        print command
        if command == "Escutando...":
            self.recognizer.listen()
        elif command == "Pausado":
            self.recognizer.pause()
        elif command == "Escutando continuamente":
            self.continuous_listen = True
            self.recognizer.listen()
        elif command == "Modo continuo pausado":
            self.continuous_listen = False
            self.recognizer.pause()
        elif command == "Sair":
            self.quit()

    #carregar arquivos de recursos, icons
    def load_resource(self, string):
        local_data = os.path.join(os.path.dirname(__file__), 'data')
        paths = ["/usr/share/pomeu/", "/usr/local/share/pomeu", local_data]
        for path in paths:
            resource = os.path.join(path, string)
            if os.path.exists(resource):
                return resource
        #se nao encontrado, return false/ if false, no resource was found
        return False


#parametros de inicializacao da interface #eng
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--interface", type="string", dest="interface",
                      action='store',
                      help="Interface a ser usada: 'q' para Qt")
    parser.add_option("-c", "--continuous",
                      action="store_true", dest="continuous", default=False,
                      help="inicia o software com modo 'continuo' ativado")
    parser.add_option("-H", "--history", type="int",
                      action="store", dest="history",
                      help="numero de comandos para armazenar no historico")
    parser.add_option("-m", "--microphone", type="int",
                      action="store", dest="microphone", default=None,
                      help="Especificar a entrada do microfone a ser usada (quando nao encontrada pelo sistema)")

    (options, args) = parser.parse_args()
    #criacao do objeto "pomeu"
    pomeu = Pomeu(options)
    #inicia thread do gobject
    gobject.threads_init()
    #evento main loop
    main_loop = gobject.MainLoop()
    #handle sigint #emiti sigint
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    #executar o app!
    pomeu.run()

    #executa loop principal
    try:
        main_loop.run()
    except:
        print "time to quit, hora de sair..."
        print "excessao encontrada, saindo..."
        main_loop.quit()
        sys.exit()

