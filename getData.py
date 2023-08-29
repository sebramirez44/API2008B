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