import os  # Add this import
import logging
import torch
import torch.hub
import soundfile as sf
import numpy as np
import openunmix
import librosa

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

def load_audio_file(file_path):
    try:
        logging.info(f"Loading audio file: {file_path}")
        
        if not os.path.exists(file_path):
            logging.error(f"File does not exist: {file_path}")
            return None, None

        audio_data, sample_rate = sf.read(file_path)
        logging.info(f"Read audio file: {file_path}")

        if audio_data.ndim == 1:  # if audio is mono
            logging.info("Audio data is mono, duplicating channels")
            audio_data = np.stack([audio_data, audio_data])  # duplicate the channel to make it stereo

        if sample_rate != 44100:  # if sample rate is not 44100 Hz
            logging.info("Resampling audio data to 44100 Hz")
            audio_data = librosa.resample(audio_data, sample_rate, 44100)  # resample to 44100 Hz
            sample_rate = 44100

        return audio_data, sample_rate
    except Exception as e:
        logging.error(f"Error loading audio file {file_path}: {e}")
        return None, None


def process_audio_file(file_path, sources, model, device, output_dir):
    try:
        audio_data, sample_rate = load_audio_file(file_path)
        audio_data = audio_data.T  # transpose the audio data
        audio_tensor = torch.from_numpy(audio_data).float().to(device)  # convert to Float here
        audio_tensor = audio_tensor[None, ...]  # add batch dimension
        separator = torch.hub.load('sigsep/open-unmix-pytorch', model, device=device)
        estimates = separator(audio_tensor)  # no need to convert to Double here

        source_names = ['vocals', 'drums', 'bass', 'other']
        for i, source_name in enumerate(source_names):
            if source_name in sources:
                source_audio = estimates[0, i, :, :].detach().cpu().numpy()  # convert to numpy
                output_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}_{source_name}.wav"  # changed file_name to os.path.basename(file_path)
                output_path = os.path.join(output_dir, output_filename)  # changed './output' to output_dir
                sf.write(output_path, source_audio.T, sample_rate)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
