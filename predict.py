import numpy as np
import tensorflow as tf
from tensorflow.compat.v1.keras.backend import set_session
from keras.preprocessing.image import load_img, img_to_array
import json
sess = tf.compat.v1.Session()
graph = tf.compat.v1.get_default_graph()
class IA:
    def __init__(self):
      self.longitud, self.altura = 224, 224
      modelo = './plantas/modelo/AlexNetModel.hdf5'
      set_session(sess)
      self.cnn = tf.keras.models.load_model(modelo)

    def predict(self, file):
      x = load_img(file, target_size=(self.longitud, self.altura))
      x = img_to_array(x)
      x = np.expand_dims(x, axis=0)
      x = x/255
      with graph.as_default():
        set_session(sess)
        array = self.cnn.predict(x)
      
      result = array[0]
      answer = np.argmax(result)
      print(result)
      print(answer)
      indexs=result.argsort()[-3:][::-1]
      aux=[]
      index=[]
      for i,e in enumerate(indexs):
        for t,j in enumerate(result):
          if e == t:
            j = j*100
            if(j>0.009):
              j=format(j, '.3f')
              aux.append(str(j))
              index.append(e)
      print(aux)
      print(indexs)
      li=['Manzana>Malus_domestica>Sarna_del_Manzano(Venturia_inaequalis)', 'Manzana>Malus_domestica>Podredumbre_Negra(Botryosphaeria obtusa)'
      , 'Manzana>Malus_domestica>Gymnosporangium juniperi-virginianae', 'Manzana>Malus_domestica>Saludable'
      , 'Arándano>Vaccinium_corymbosum>Saludable', 'Cereza>Rainer>Podosphaera_pannosa', 'Cereza>Rainer>Saludable'
      , 'Maíz>Zea_mays>Mancha_gris(Cercospora_zeae-maydis)', 'Maíz>Zea_mays>Roya_común(Puccinia_sorghi)'
      , 'Maíz>Zea_mays>Tizón_de_la_hoja(Exserohilum_turcicum)', 'Maíz>Zea_mays>Saludable', 'Uva>Vitis_rotundifolia>Podredumbre_Negra(Guignardia_bidwellii)'
      , 'Uva>Vitis_rotundifolia>Phaeomoniella_aleophilum', 'Uva>Vitis_rotundifolia>Tizón(Pseudocercospora_vitis)', 'Uva>Vitis_rotundifolia>Saludable'
      , 'Naranja>Citrus_sinensis>Huanglongbing', 'Pera>Pyrus_communis>Xanthomonas_campestris', 'Pera>Pyrus_communis>Saludable'
      , 'Ají>Capsicum_annuum>Xanthomonas_campestris', 'Ají>Capsicum_annuum>Saludable', 'Papa>Solanum_tuberosum>Tizón_temprano(Alternaria_solani)'
      , 'Papa>Solanum_tuberosum>Tizón_tardío(Phytophthora_infestans)', 'Papa>Solanum_tuberosum>Saludable'
      , 'Frambuesa>Rubus_idaeus>Saludable', 'Soja>Glycine_max>Saludable'
      , 'Calabaza>Cucurbita_ficifolia>Oídio(Erysiphe_cichoracearum)', 'Fresa>Fragaria_vesca>Diplocarpon_earlianum', 'Fresa>Fragaria_vesca>Saludable'
      , 'Tomate>Solanum_lycopersicum>Xanthomonas_campestris', 'Tomate>Solanum_lycopersicum>Tizón_Temprano(Alternaria_solani)'
      , 'Tomate>Solanum_lycopersicum>Tizón_tardío(Phytophthora_infestans)', 'Tomate>Solanum_lycopersicum>Cladosporiosis(Fulvia_fulva)'
      , 'Tomate>Solanum_lycopersicum>Mancha_de_hoja(Septoria_lycopersici)', 'Tomate>Solanum_lycopersicum>Ácaro_rojo(Tetranychus_urticae)'
      , 'Tomate>Solanum_lycopersicum>Mancha_anillada(Corynespora_cassiicola)'
      , 'Tomate>Solanum_lycopersicum>TYLCV(Yellow_Leaf_Curl_Virus)', 'Tomate>Solanum_lycopersicum>TOMV(Virus_del_Mosaico)', 'Tomate>Solanum_lycopersicum>Saludable']
      
      enfermedades=[]
      for i,e in enumerate(index):
        for t,j in enumerate(li):
          if e == t:
            enfermedades.append(j)
      print(enfermedades)  
      print(li[answer])  
      lista=[]
      cadena = []
      for i,x in enumerate(enfermedades):
        cadena=x.split('>')
        lista.append({'planta':cadena[0],'especie':cadena[1],'enfermedad':cadena[2],'porc':aux[i]})
      return json.dumps(lista)
