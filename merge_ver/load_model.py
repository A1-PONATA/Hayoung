
from tensorflow.python.keras.models import model_from_yaml
import os
import tensorflow as tf

os.environ["CUDA_VISIBLE_DEVICES"] = "1"  # Or 2, 3, etc. other than 0

# On CPU/GPU placement
config = tf.compat.v1.ConfigProto(allow_soft_placement=True, log_device_placement=True)
config.gpu_options.allow_growth = True
tf.compat.v1.Session(config=config)


def load_model(path):
    yamlPath =path[0]
    h5Path = path[1]

    yaml_file1 = open(yamlPath, 'r')
    loaded_model_yaml = yaml_file1.read()
    yaml_file1.close()
    model = model_from_yaml(loaded_model_yaml)

    # load weights into new model
    model.load_weights(h5Path)
    model._make_predict_function()

    return model

print(load_model(['/home/pirl/A1-PONATA/Hayoung/motion_model_test/mm_v3.yaml',
            '/home/pirl/A1-PONATA/Hayoung/motion_model_test/mm_v3.h5']))



# print(load_model(['/home/pirl/A1-PONATA/Hayoung/lane_model_test/lane_model_v3-1.yaml',
#  '/home/pirl/A1-PONATA/Hayoung/lane_model_test/lane_model_v3-1.h5']))

# import tensorflow as tf
#
# print(tf.__version__)