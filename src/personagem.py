from math import floor
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json

class Personagem:
    def __init__(self, classes:dict, nome:str = "N/a") -> None:
        self.nome = nome
        self.raca = ''
        self.classes = classes
        self.nivel = 0
        for i in self.classes:
            self.nivel += self.classes[i]
        
        
        self.atributos = {
            "for" : 0,
            "des" : 0,
            "con" : 0,
            "int" : 0,
            "sab" : 0,
            "car" : 0,
            "hon" : 0
        }
        self.pericias = list()
        self.talentos = list()
        self.habilidades = list()
        self.jutsus = list()
        self.armadura = dict()
    
    def modAtributo(self, valorAtributo:int) -> int:
        return floor((valorAtributo-10)/2)
    
    def ca(self) -> int:
        if self.armadura is not  None:
            desBonus = self.modAtributo(self.atributos["des"])
            armaduraBonus = 0
        else:
            desBonus = min(self.armadura['limiteDes'], self.modAtributo(self.atributos["des"]))
            armaduraBonus = self.armadura["defesa"]
        ca = 10 + floor(self.nivel/2) + desBonus + armaduraBonus
        return ca
        
    def gerarAtributosPadrao(self, prioridade:list) -> None:
        """adiciona os numeros 17, 15, 13, 12, 10 e 8 nos atributos seguindo uma lista de prioridade, exceto honra, que é definido como 14 por padrão

        Args:
            prioridade (list): uma lista com os nomes dos atributos abreviados
        """
        
        numeros = (17, 15, 13, 12, 10, 8)
        self.atributos["hon"] = 14
        
        for i in range(6):
            self.atributos[str(prioridade[i])] = numeros[i]
        print(f'\natributos padrao ficaram {self.atributos}')
    
    def escolherRaca(self, raca:str):
        with open('src\\raca.json', 'r') as f:
            racaList = json.load(f)
        self.racaData = racaList[raca]
        
        #bonus de atributo
        bonus = self.racaData["atributos"]
        for i in self.atributos:
            for j in bonus:
                if i == j:
                    self.atributos[i] += bonus[j]
        print(f'\n\ncom os bonus da raca {self.atributos}')

        #habilidades
        hab = self.racaData["habilidades"]
        for i in hab:
            self.habilidades.append(i)
        
        self.raca = self.racaData["nome"]
        print(f'\ncom as habilidades de raca {self.habilidades}')
        
    
    def vestirArmadura(self, nomeArmadura:str, defesa:int, limiteDes:int= None, penalidade:int = 0):
        self.armadura = dict()
        self.armadura['nome'] = nomeArmadura
        self.armadura['defesa'] = defesa
        self.armadura['limiteDes'] = limiteDes
        self.armadura['penalidade'] = penalidade
     
    def printaFicha(self) -> None:
        print(f"\n\n =========={self.nome.upper()}===========")
        
        classes = [f'{k.capitalize()} {v}' for k, v in self.classes.items()]
        classesNivel = " ".join(classes)
        print(f"{self.raca}, {classesNivel}, ND {self.nivel}")
        
        for i in self.atributos:
            print(f'{i.capitalize()}: {self.atributos[i]} ({self.modAtributo(self.atributos[i])})')
        
        print(f"\nPV 0, PM 0, CA {self.ca()}")
    
    def enviarFicha(self):
        driver = Driver()
        
        #nome
        driver.doField("pdfjs_internal_id_67R", self.nome)
        
        #raça
        driver.doField("pdfjs_internal_id_69R", self.raca)
        
        #classes
        classes = [f'{k.capitalize()} {v}' for k, v in self.classes.items()]
        driver.doField('pdfjs_internal_id_70R', classes)
        
        #atributos
        driver.doField("pdfjs_internal_id_86R", self.atributos['for'])
        driver.doField("pdfjs_internal_id_87R", self.modAtributo(self.atributos['for']))     
        
        driver.doField("pdfjs_internal_id_96R", self.atributos['des'])
        driver.doField("pdfjs_internal_id_97R", self.modAtributo(self.atributos['des']))
        
        driver.doField("pdfjs_internal_id_106R", self.atributos['con'])
        driver.doField("pdfjs_internal_id_107R", self.modAtributo(self.atributos['con']))
        
        driver.doField("pdfjs_internal_id_116R", self.atributos['int'])
        driver.doField("pdfjs_internal_id_117R", self.modAtributo(self.atributos['int']))
        
        driver.doField("pdfjs_internal_id_126R", self.atributos['sab'])
        driver.doField("pdfjs_internal_id_127R", self.modAtributo(self.atributos['sab']))
        
        driver.doField("pdfjs_internal_id_136R", self.atributos['car'])
        driver.doField("pdfjs_internal_id_137R", self.modAtributo(self.atributos['car']))
        
        driver.doField("pdfjs_internal_id_146R", self.atributos['hon'])
        driver.doField("pdfjs_internal_id_147R", self.modAtributo(self.atributos['hon']))
        
    
    
class Driver(webdriver.Firefox):
    def __init__(self) -> None:
        super().__init__()
        self.get("file:///C:/Users/lucas/Downloads/ficha-editavel-imperio-de-jade-2.pdf")

    def doField(self, fieldId:str, keys:str):
        #time.sleep(1)
        field = self.find_element(By.ID, fieldId)
        field.click()
        #time.sleep(1)
        field.send_keys(keys)
        #time.sleep(1)



kyu = Personagem(nome ='Kyu Ren', classes={"kensei": 1, "ninja": 3})
l = ['for', 'con', 'sab', 'int', 'car', 'des']
kyu.gerarAtributosPadrao(l)
kyu.escolherRaca('hanyo')
kyu.printaFicha()
kyu.enviarFicha()

    
       
       
        
#requisitos
# esse app vai preencher uma ficha automáticamente usando opdf Fill
# o escolhe a classe, nível, e raça, além de atributos
#ter opção de gerar atributos recomendados
#o programa vei ser operado em hard coding por enquanto. em algum momento, será implementada a função de interface
# não vai ter descrições do jogo no app, apenas nomes das classes e talentos        