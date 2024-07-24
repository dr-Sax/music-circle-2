from basic_pitch.inference import predict_and_save, Model
from basic_pitch import ICASSP_2022_MODEL_PATH
import os.path

basic_pitch_model = Model(ICASSP_2022_MODEL_PATH)

path = 'media/twinkle.wav'
path2 = 'media'

print(os.path.isdir(path))
predict_and_save(audio_path_list = [path], 
                 output_directory = path2, 
                 save_midi = True, 
                 sonify_midi = True, 
                 save_model_outputs = True, 
                 save_notes = True,
                 model_or_model_path = basic_pitch_model
                 )
