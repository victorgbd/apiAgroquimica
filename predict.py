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
      li=['6>Manzana>3>Malus_domestica>1>Sarna_del_Manzano(Venturia_inaequalis)', '6>Manzana>3>Malus_domestica>2>Podredumbre_Negra(Botryosphaeria obtusa)'
      , '6>Manzana>3>Malus_domestica>3>Gymnosporangium juniperi-virginianae', '6>Manzana>3>Malus_domestica>-1>Saludable'
      , '7>Arándano>4>Vaccinium_corymbosum>-1>Saludable', '5>Cereza>5>Rainer>5>Podosphaera_pannosa', '5>Cereza>5>Rainer>-1>Saludable'
      , '4>Maíz>6>Zea_mays>6>Mancha_gris(Cercospora_zeae-maydis)', '4>Maíz>6>Zea_mays>7>Roya_común(Puccinia_sorghi)'
      , '4>Maíz>6>Zea_mays>8>Tizón_de_la_hoja(Exserohilum_turcicum)', '4>Maíz>6>Zea_mays>-1>Saludable', '3>Uva>7>Vitis_rotundifolia>9>Podredumbre_Negra(Guignardia_bidwellii)'
      , '3>Uva>7>Vitis_rotundifolia>10>Phaeomoniella_aleophilum', '3>Uva>7>Vitis_rotundifolia>11>Tizón(Pseudocercospora_vitis)', '3>Uva>Vitis_rotundifolia>-1>Saludable'
      , '2>Naranja>8>Citrus_sinensis>12>Huanglongbing', '8>Pera>9>Pyrus_communis>13>Xanthomonas_campestris', '8>Pera>9>Pyrus_communis>-1>Saludable'
      , '9>Ají>10>Capsicum_annuum>13>Xanthomonas_campestris', '9>Ají>10>Capsicum_annuum>-1>Saludable', '10>Papa>11>Solanum_tuberosum>14>Tizón_temprano(Alternaria_solani)'
      , '10>Papa>11>Solanum_tuberosum>15>Tizón_tardío(Phytophthora_infestans)', '10>Papa>11>Solanum_tuberosum>-1>Saludable'
      , '11>Frambuesa>12>Rubus_idaeus>-1>Saludable', '12>Soja>13>Glycine_max>-1>Saludable'
      , '13>Calabaza>14>Cucurbita_ficifolia>16>Oídio(Erysiphe_cichoracearum)', '14>Fresa>15>Fragaria_vesca>17>Diplocarpon_earlianum', '14>Fresa>15>Fragaria_vesca>-1>Saludable'
      , '1>Tomate>1>Solanum_lycopersicum>13>Xanthomonas_campestris', '1>Tomate>1>Solanum_lycopersicum>14>Tizón_Temprano(Alternaria_solani)'
      , '1>Tomate>1>Solanum_lycopersicum>15>Tizón_tardío(Phytophthora_infestans)', '1>Tomate>1>Solanum_lycopersicum>18>Cladosporiosis(Fulvia_fulva)'
      , '1>Tomate>1>Solanum_lycopersicum>19>Mancha_de_hoja(Septoria_lycopersici)', '1>Tomate>1>Solanum_lycopersicum>20>Ácaro_rojo(Tetranychus_urticae)'
      , '1>Tomate>1>Solanum_lycopersicum>21>Mancha_anillada(Corynespora_cassiicola)'
      , '1>Tomate>1>Solanum_lycopersicum>22>TYLCV(Yellow_Leaf_Curl_Virus)', '1>Tomate>1>Solanum_lycopersicum>23>TOMV(Virus_del_Mosaico)', '1>Tomate>1>Solanum_lycopersicum>-1>Saludable']
      
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
        lista.append({'codplanta':cadena[0],'planta':cadena[1],'codespecie':cadena[2],'especie':cadena[3],'codenfer':cadena[4],'enfermedad':cadena[5],'porc':aux[i]})
      return json.dumps(lista)
