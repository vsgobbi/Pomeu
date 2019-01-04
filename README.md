#POMEU (Program of a Meanness User)

POMEU é um aplicativo de reconhecimento de voz automatico, utilizado para controle e comando em ambiente linux/x11, 
desenvolvido no Ubuntu 12.04 com Qt 4.8.1, PySide 1.2.2 e Python 2.7.
Direitos: LPGL, modificação do software open source Blather, por Vitor Sgobbi, 2014, ICEA (Air Traffic Control Institute).
Versão de release em desenvolvimento para codificador pocketsphinx (CMU) em Inglês nativo.
#Description
POMEU is a speech recognizer working as control and command under linux terminal interface, constructed on Ubuntu and intended for Debian distributions users. When a user speaks a preset sentence you do nice things! Configure and use a simple command parser file.

##Pré-requisitos /Requirements
1. pocketsphinx
2. gstreamer-0.10 (and what ever plugin has pocket sphinx support)
3. gstreamer-0.10 base plugins
4. pyside (only required for the Qt based UI)
5. pygtk (only required for the Gtk based UI)
6. pyyaml (only required for reading the options file)

##Como usar / How to use it
0. Mover o arquivo de comandos "commands.tmp" para a pasta raiz do software.
Preencher os comandos a serem executados seguindo a sintaxe de exemplo, após alterar o arquivo salvar como "commands.conf".

OBS: PARA ESTE MODELO É POSSÍVEL SOMENTE DECODIFICIAR SENTENÇAS EM INGLÊS.
O MODELO EM PORTUGUÊS AINDA ESTÁ SENDO DESENVOLVIDO.

Move file "commands.tmp" to "commands.conf" in the same application's folder and fill the file with sentences and command to be run only on english language.

1. Executar Pomeu.py (de preferência utilizando Python 2.7), Pomeu irá gerar o arquivo corpus "sentence.corpus" contendo as sentencas do arquivo "commands.conf".

Run Pomeu.py, this will generate the file "sentences.corpus" based on sentences in the 'commands' file.

2. fechar o Pomeu / quit Pomeu.

3. fazer upload do arquivo de corpus (sentence.corpus) no site da universidade de Carnegie Mellon University: <http://www.speech.cs.cmu.edu/tools/lmtool.html>

Go upload to <http://www.speech.cs.cmu.edu/tools/lmtool.html> the sentences.corpus file

4. Baixar os arquivos de extensão ".lm" e ".dic" para a pasta "language" do aplicativo e renomeie somente como "lm" e "dic".

Download the resulting ".lm" file to language directory and rename to file to 'lm'

5. download the resulting ".dic" file to the language directory and rename it file to 'dic'.

6. Executar ./Pomeu.py -i q -c (Modo continuo)

Run Pomeu.py
    * for Qt GUI, run Pomeu.py -i q
    * to start a UI in 'continuous' listen mode, use the -c flag
    * to use a microphone other than the system default, use the -m flag

7. Diga as sentencas criadas.

Start talking, enjoy it.

**Note:** To start Pomeu without needing to enter command line options all the time, copy "options.yaml.tmp" to "options.yaml" and edit accordingly.
You may not need to exhastively list all possible sentences: the decoder will allow fragments to recombine into new sentences.

###Bonus
once the sentences.corpus file has been created, run the language_updater.sh script to automate the process of creating and downloading language files.


Para rodar sem interface grafica confiurando onde o dispositivo do microfone conectado esta:
`./Pomeu.py -m 2`

###Finding the Device Number of a USB microphone
There are a few ways to find the device number of a USB microphone.

* `cat /proc/asound/cards`
* `arecord -l`
