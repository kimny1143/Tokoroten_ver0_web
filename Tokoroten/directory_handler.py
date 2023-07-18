import os
import logging
from . import audio_processing as ap

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

def process_directory(input_dir, sources, model, device, output_dir):
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.wav'):
            file_path = os.path.join(input_dir, file_name)
            logging.info(f"Processing file: {file_path}")
            try:
                ap.process_audio_file(file_path, sources, model, device, output_dir)
            except Exception as e:
                logging.error(f"Error processing file {file_path}: {e}")
