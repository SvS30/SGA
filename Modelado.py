class Modelo:
  """Clase para almacenar la configuración o modelación del sistema
  """
  def __init__(self, config):
    self.poblacion_inicial = config['pob_ini']
    self.poblacion_max = config['pob_max']
    self.generaciones = config['generaciones']
    self.abscisa_min = config['abscisa_min']
    self.abscisa_max = config['abscisa_max']
    self.ordenada_min = config['ordenada_min']
    self.ordenada_max = config['ordenada_max']
    self.error_perm = config['error_perm']
    self.mutacion_gen = config['mutacion_gen']
    self.mutacion_individuo = config['mutacion_individuo']

  def get_poblacion_inicial(self):
    return self.poblacion_inicial

  def get_poblacion_maxima(self):
    return self.poblacion_max

  def get_generaciones(self):
    return self.generaciones

  def get_abscisa_min(self):
    return self.abscisa_min

  def get_abscisa_max(self):
    return self.abscisa_max

  def get_ordenada_min(self):
    return self.ordenada_min

  def get_ordenada_max(self):
    return self.ordenada_max
  
  def get_error_perm(self):
    return self.error_perm

  def get_mutacion_gen(self):
    return self.mutacion_gen

  def get_mutacion_individuo(self):
    return self.mutacion_individuo
