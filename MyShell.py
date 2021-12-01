import cmd, subprocess, sys, logging
from sympy import *

logging.basicConfig( filename="MyShell.log", level=logging.DEBUG )

class MyShell(cmd.Cmd):
    intro = "Benvenuto nella shell di Mastyx. \n"
    prompt = "->> "

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.namespace = {}

    def do_quit(self, line):
        """ Esce dal programma"""
        print("\nGrazie per aver usato MastyxShell !")
        sys.exit(1)

    def do_shell(self, line):
        """Esegue il comando shell di sistema"""
        try:
            subprocess.call(line, timeout=5, shell=True)
        except subprocess.TimeoutExpired:
            print("Il processo non è terminato nei tempi richiesti ! ")

    def emptyline(self):
        """ Non fare nulla se la linea e vuota """
        pass

    def do_EOF(self, line):
        self.do_quit(line)

    do_q = do_quit

    def precmd(self, line):
        """Azioni prima di interpretare il comando """
        self.raw_line = line
        try :
            return line.format_map(self.namespace)
        except KeyError as ex :
            print(f"L'etichetta {ex} non è definita !")
        except ValueError:
            print("L'etichetta tra parentesi graffe non può essere un numero")

        return "" # restituisce una linea vuota

    def default(self, line):
        """I comandi non previsti nell'help vengono semplificati con Sympy"""
        try :
            if '=' in line :
                try:
                    n, e = [item.strip() for item in line.split("=")]
                except ValueError:
                    print("Non è possibile fare più di un asegnamento nello stesso comando")
                else :
                    if n.isalnum():
                        self.namespace.update({n:e})
                    else :
                        print(f"Nome {n}")
            elif line == self.raw_line and line.isalnum():
                print("Prova con {%s} piuttosto che con %s !" %(line, line))
            else:
                print(simplify(line) if line else "")
        except Exception as ex:
            logging.debug(f"Linea: {line}")
            logging.debug(f"Messaggio: {ex}\n")
            print(ex)

    def help_default(self):
        print(self.default.__doc__)


if __name__ == "__main__":
    pws = MyShell()
    pws.cmdloop()
