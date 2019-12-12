
from tensorflow.python.keras.models import model_from_yaml

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

print(load_model(['/home/pirl/A1-PONATA/Hayoung/motion_model_test/motion_model_demoV2-1.yaml',
            '/home/pirl/A1-PONATA/Hayoung/motion_model_test/motion_model_demoV2-1.h5']))