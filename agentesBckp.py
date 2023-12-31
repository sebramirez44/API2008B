# visualizacion no carga bien para mi, como que se abre la ventana pero no hay nada y se cierra no se si imnporte.
import mesa
from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import SingleGrid

# Data visualization tools.
import seaborn as sns

# Has multi-dimensional arrays and matrices. Has a large collection of
# mathematical functions to operate on these arrays.
import numpy as np

# Data manipulation and analysis.
import pandas as pd

# los objetos de tipo contenedor tienen peso, estatus y tamaño.
class Contenedor:
  def __init__(self, weight, status, size):
    self.weight = weight
    self.status = status
    self.size = size

class Barco(Agent):
  def __init__(self, unique_id, model):
    super().__init__(unique_id, model)
    self.contenedores = []
    self.crearContenedores(10)
    # tenemos un atributo que ve la cantidad de contenedores porque luego podriamos cambiarlo a cuatro listas de contenedores.
    self.cantContenedores = len(self.contenedores)

  # función de movimiento
  def movimiento(self):
    x, y = self.pos
    #

    cellmates = []
    cellmates.append(self.model.grid.get_cell_list_contents([(x+1, y-3)]))
    cellmates.append(self.model.grid.get_cell_list_contents([(x+1, y-2)]))
    cellmates.append(self.model.grid.get_cell_list_contents([(x+1, y-1)]))
    cellmates.append(self.model.grid.get_cell_list_contents([(x+1, y)]))

    isGrua = False


    # mientras que su neighbor de la izquiera no sea una grua
    if len(cellmates[3]) > 0:
      if isinstance(cellmates[3][0], GruaPortico):
        isGrua = True

    if isGrua == False or len(self.contenedores) == 0:
      if y != 0:
        y  = y - 1

    elif isGrua == True:
      # quitar los contenedores del barco y darselos a la grua, uno cada step
      for i in range(0,4):
        if len(self.contenedores) != 0:
          if len(cellmates[i]) > 0 and cellmates[i][0].cargando == False:
            contenedorMoviendo = self.contenedores.pop()
            #print("pasamos un contenedor")
            cellmates[i][0].contenedores.append(contenedorMoviendo)

    new_position = (x,y)
    self.model.grid.move_agent(self, new_position)

  def crearContenedores(self, n):
    # no me acueredo bien si estos eran los status posibles
    statusPosibles = ["Exportacion", "Importacion"]

    for i in range(n):
      # cambiar esto a otros valores probablemente
      peso = self.random.randint(1,10)
      # tambien cambiar el size a otra cosa
      size = self.random.choice([20, 40])

      contenedor = Contenedor(peso, self.random.choice(statusPosibles), size)
      self.contenedores.append(contenedor)
    # peso numero random por ahora
    # status
    # tamaño

  def step(self):
    self.movimiento()
    # print(f"tengo {len(self.contenedores)} contenedores.")

# No estoy seguro si incluir contenedores en el constructor o solo afuera.
class GruaRTG(Agent):
  def __init__(self, unique_id, model):
    super().__init__(unique_id, model)
    self.Contenedores = []
    self.destino = "Ninguno"

  def movimiento(self):
    #print(self.destino)
    #print(self.Contenedores)

    # obtener su vecino de abajo, si es el del medio no hacer movimiento por ahora e implementar otra logica.
    xE = 6
    yE = 5
    xA = 14
    yA = 6
    xV = 14
    yV = 9
    xExpo = 14
    yExpo = 2

    x,y = self.pos
    celda_enfrente = self.model.grid.get_cell_list_contents([(x-1, y)])
    celda_derecha = self.model.grid.get_cell_list_contents([(x, y+1)])
    celda_izquierda = self.model.grid.get_cell_list_contents([(x, y-1)])
    celda_abajo = self.model.grid.get_cell_list_contents([(x+1, y)])

    if len(self.Contenedores) == 0:
      
      if y > (yE) and len(celda_izquierda) == 0:
        y -= 1
      elif x > (xE+1) and len(celda_enfrente) == 0:
        x -= 1
      elif y < (yE) and len(celda_derecha) == 0:
        y += 1
      elif len(celda_enfrente) > 0 and isinstance(celda_enfrente[0], Explanada):
        expl = self.model.grid.get_cell_list_contents([(x-1, y)])[0]
        if len(expl.contenedores) > 0:
          cont = expl.contenedores.pop()
          self.Contenedores.append(cont)
          #print(f"soy la grua RTG {self.unique_id} y tengo el contenedor {self.Contenedores[0]}")

          # Aquí viene la lógica para decidir a donde llevar el contenedor
          if (self.Contenedores[0].status == "Exportacion"):
            self.destino = "Exportacion"
          elif (self.Contenedores[0].weight < 2 and self.Contenedores[0].size == 20) or (self.Contenedores[0].weight < 4 and self.Contenedores[0].size == 40):
            self.destino = "Vacios"
          else:
            self.destino = "Almacen"

    elif self.destino == "Almacen":
      if y > (yA) and len(celda_izquierda) == 0:
        y -= 1
      elif x < (xA-1) and len(celda_abajo) == 0:
        x += 1
      elif y < (yA) and len(celda_derecha) == 0:
        y += 1
      elif len(celda_abajo) > 0 and isinstance(celda_abajo[0], Organizacion):
        orga = celda_abajo[0]
        contenedor_a_agregar = self.Contenedores.pop()
        orga.Contenedores.append(contenedor_a_agregar)
        self.destino = "Ninguno"

    elif self.destino == "Exportacion":
      if y > (yExpo) and len(celda_izquierda) == 0:
        y -= 1
      elif x < (xExpo-1) and len(celda_abajo) == 0:
        x += 1
      elif y < (yExpo) and len(celda_derecha) == 0:
        y += 1

      elif len(celda_abajo) > 0 and isinstance(celda_abajo[0], Organizacion):
        orga = celda_abajo[0]
        contenedor_a_agregar = self.Contenedores.pop()
        #print(self.Contenedores)
        orga.Contenedores.append(contenedor_a_agregar)
        self.destino = "Ninguno"

    elif self.destino == "Vacios":
      if y > (yV) and len(celda_izquierda) == 0:
        y -= 1
      elif x < (xV-1) and len(celda_abajo) == 0:
        x += 1
      elif y < (yV) and len(celda_derecha) == 0:
        y += 1

      elif len(celda_abajo) > 0 and isinstance(celda_abajo[0], Organizacion):
        org = celda_abajo[0]
        contenedor_a_agregar = self.Contenedores.pop()
        org.Contenedores.append(contenedor_a_agregar)
        self.destino = "Ninguno"


    new_position = (x,y)
    self.model.grid.move_agent(self, new_position)



    # si la diferencia en x es de solo 1 y no tienen el mismo valor en y, se mueve uno a la izquierda primero

  def step(self):
    self.movimiento()

class GruaPortico(Agent):
  def __init__(self, unique_id, model, cargando):
    super().__init__(unique_id, model)
    self.cargando = cargando
    self.contenedores = []

  def step(self):
    # primero capturar el agente Explanada de alguna forma
    # si no esta vacia la lista de contenedores, darle uno a la explanada.
    # despues seria buena idea calcular la explanada mas cercana con nearest point y entregarle contenedores a esa.
    if self.cargando == True:
      for content in self.model.grid.coord_iter():
        agent, (x,y) = content
        if isinstance(agent, Explanada):
            # print(f"tengo {len(self.contenedores)} contenedores soy Grua")
            contenedorMoviendo = self.contenedores.pop()
            agent.contenedores.append(contenedorMoviendo)
            self.cargando = False
    if len(self.contenedores) > 0:
          self.cargando = True

class Explanada(Agent):
  def __init__(self, unique_id, model):
    super().__init__(unique_id, model)
    self.contenedores = []
  def step(self):
    pass
    #print(f"tengo {len(self.contenedores)} contenedores soy Explanada")

# agentes Vacios, Almacen, Exportando.
# no se si definirlos como un agente Organizacion con esos diferentes tipos o como tres agentes
class Organizacion(Agent):
  def __init__(self, unique_id, model, tipoContenedores):
    super().__init__(unique_id, model)
    self.tipoContenedores = tipoContenedores
    self.Contenedores = []
  def imprimo_contenidos(self):
    if self.tipoContenedores == "Almacen":
      print("-------------------------------------------")
      print("En el área de almacén hay " + str(len(self.Contenedores)) + " contenedores")
      if len(self.Contenedores) > 0:
        for contenedor in self.Contenedores:
          print("peso: " + str(contenedor.weight) + ", tamaño: " + str(contenedor.size) + ", estatus: " + str(contenedor.status))
    if self.tipoContenedores == "Vacios":
      print("-------------------------------------------")
      print("En el área de vacíos hay " + str(len(self.Contenedores)) + " contenedores")
      if len(self.Contenedores) > 0:
        for contenedor in self.Contenedores:
          print("peso: " + str(contenedor.weight) + ", tamaño: " + str(contenedor.size) + ", estatus: " + str(contenedor.status))
    if self.tipoContenedores == "Exportados":
      print("-------------------------------------------")
      print("En el área de exportados hay " + str(len(self.Contenedores)) + " contenedores")
      if len(self.Contenedores) > 0:
        for contenedor in self.Contenedores:
          print("peso: " + str(contenedor.weight) + ", tamaño: " + str(contenedor.size) + ", estatus: " + str(contenedor.status))


class Puerto(Model):
  def __init__(self):
    # cambiar width y height
    self.lista_master_agentes = []
    self.width = 20
    self.height = 14
    self.schedule = SimultaneousActivation(self)
    self.grid = SingleGrid(self.width, self.height, False)
    # cambiar la posicion donde va el barco
    barco = Barco(0, self)
    # si x y y empiezan en 0
    x = 2
    y = 13
    self.schedule.add(barco)
    self.lista_master_agentes.append(barco)
    self.grid.place_agent(barco, (x,y))
    # declaro otros x y y por si acaso

    #------------------------------------
    #       Grúas de pórtico
    gruaP1 = GruaPortico("p1",self, False)
    x1 = 3
    y1 = 4
    self.schedule.add(gruaP1)
    self.lista_master_agentes.append(gruaP1)
    self.grid.place_agent(gruaP1, (x1, y1))
    gruaP2 = GruaPortico("p2",self, False)
    self.schedule.add(gruaP2)
    self.lista_master_agentes.append(gruaP2)
    self.grid.place_agent(gruaP2, (3, 5))
    gruaP3 = GruaPortico("p3",self, False)
    self.schedule.add(gruaP3)
    self.lista_master_agentes.append(gruaP3)
    self.grid.place_agent(gruaP3, (3, 6))
    gruaP4 = GruaPortico("p4",self, False)
    self.schedule.add(gruaP4)
    self.lista_master_agentes.append(gruaP4)
    self.grid.place_agent(gruaP4, (3, 7))
    #------------------------------------

    explanada = Explanada(2, self)
    x2 = 6
    y2 = 5
    self.schedule.add(explanada)
    self.lista_master_agentes.append(explanada)
    self.grid.place_agent(explanada, (x2, y2))

    gruaRTG = GruaRTG(3, self)
    x3 = 13
    y3 = 2
    self.schedule.add(gruaRTG)
    self.lista_master_agentes.append(gruaRTG)
    self.grid.place_agent(gruaRTG, (x3, y3))

    self.exportados = Organizacion(4, self, "Exportados")
    x4 = 14
    y4 = 2
    self.schedule.add(self.exportados)
    self.lista_master_agentes.append(self.exportados)
    self.grid.place_agent(self.exportados, (x4, y4))
    gruaRTG2 = GruaRTG(5, self)
    x5 = 13
    y5 = 6
    self.schedule.add(gruaRTG2)
    self.lista_master_agentes.append(gruaRTG2)
    self.grid.place_agent(gruaRTG2, (x5, y5))
    self.almacen = Organizacion(6, self, "Almacen")
    x6 = 14
    y6 = 6
    self.schedule.add(self.almacen)
    self.lista_master_agentes.append(self.almacen)
    self.grid.place_agent(self.almacen, (x6, y6))
    self.vacios = Organizacion(7, self, "Vacios")
    x7 = 14
    y7 = 9
    self.schedule.add(self.vacios)
    self.lista_master_agentes.append(self.vacios)
    self.grid.place_agent(self.vacios, (x7, y7))
    gruaRTG3 = GruaRTG(8, self)
    x8 = 13
    y8 = 9
    self.schedule.add(gruaRTG3)
    self.lista_master_agentes.append(gruaRTG3)
    self.grid.place_agent(gruaRTG3, (x8, y8))

    # para el API ya no necesitamos un datacollector, solo la funcion para llamar desde main.

  def get_data(self):
    # si el agente es barco, cant contenedores
    # arreglo de contenedores
    data = {}
    # Barco: {
    #   cantContenedores: int
    #   arregloContenedores: Contenedor[]
    # }
    # gruaP: {
    #   cargando: bool
    #   cantConenedores: int
    #   arregloContenedores: Contenedor[]
    # }
    # explanada: {
    #   arregloContenedores: Contenedor[]
    #   cantContenedores: int
    # }
    # gruaRTG: {
    #   arregloContenedores: Contenedor[]
    #   Destino: [Ninguno, Exportacion, Vacios, Almacen, Home]
    #   posicion (x, y)
    # }

    for agent in self.lista_master_agentes:
      if isinstance(agent, Barco):
        contenedores_dict = []
        for contenedorOrg in agent.contenedores:
          contenedor = {
            "weight" : contenedorOrg.weight,
            "size" : contenedorOrg.size,
            "status" : contenedorOrg.status
          }
          # contenedor["weight"] = contenedorOrg.weight
          # contenedor["size"] = contenedorOrg.size
          # contenedor["status"] = contenedorOrg.status
          contenedores_dict.append(contenedor)
        agent_data = {
          "cantContenedores": len(agent.contenedores),
          # crear una nueva lista contenedores con diccionarios que tienen el valor del contenedor
          "arregloContenedores": contenedores_dict
        }
        data[agent.unique_id] = agent_data
      elif isinstance(agent, GruaPortico):
        contenedores_dict = []
        for contenedorOrg in agent.contenedores:
          contenedor = {
            "weight": contenedorOrg.weight,
            "size" : contenedorOrg.size,
            "status" : contenedorOrg.status
          }
          contenedores_dict.append(contenedor)
        agent_data = {
          "cargando": agent.cargando,
          "cantContenedores": len(agent.contenedores),
          "arregloContenedores": contenedores_dict
        }
        data[agent.unique_id] = agent_data
      elif isinstance(agent, Explanada):
        contenedores_dict = []
        for contenedorOrg in agent.contenedores:
          contenedor = {
            "weight": contenedorOrg.weight,
            "size": contenedorOrg.size,
            "status": contenedorOrg.status
          }
          contenedores_dict.append(contenedor)
        agent_data = {
          "cantContenedores": len(agent.contenedores),
          "arregloContenedores": contenedores_dict
        }
        data[agent.unique_id] = agent_data
      elif isinstance(agent,  GruaRTG):
        contenedores_dict = []
        # gruaRTG tiene atributo contenedores con mayuscula, tal vez cambiarlo si es mas problema
        for contenedorOrg in agent.Contenedores:
          contenedor = {
            "weight": contenedorOrg.weight,
            "size": contenedorOrg.size,
            "status": contenedorOrg.status
          }
          contenedor_dict.append(contenedor)
        x,y = agent.pos
        agent_data = {
          "cantContenedores": len(agent.Contenedores),
          "destino": agent.destino,
          "posX": x,
          "posY": y,
          "arregloContenedores" : contenedores_dict
        }
        data[agent.unique_id] = agent_data
      elif isinstance(agent, Organizacion):
        contenedores_dict = []
        for contenedorOrg in agent.Contenedores:
          contenedor = {
            "weight": contenedorOrg.weight,
            "size": contenedorOrg.size,
            "status": contenedorOrg.status
          }
          contenedor_dict.append(contenedor)
        agent_data = {
          "cantContenedores": len(agent.Contenedores),
          "arregloContenedores" : contenedores_dict
        }
        data[agent.unique_id] = agent_data
        # checar que tipo es para mandar eso
    return data

  def step(self):
    # self.datacollector.collect(self)
    self.schedule.step()

  def imprimo(self):
    self.almacen.imprimo_contenidos()
    self.exportados.imprimo_contenidos()
    self.vacios.imprimo_contenidos()
