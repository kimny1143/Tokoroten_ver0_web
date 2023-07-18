import os
import argparse
import logging
import directory_handler as dh # Import the directory handler
import certifi

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)


def parse_and_process():
    # Set the SSL_CERT_FILE environment variable
    os.environ['SSL_CERT_FILE'] = certifi.where()

    parser = argparse.ArgumentParser(description='Select the parts for source separation.')
    # same argument setup as before
    args = parser.parse_args()

    sources = args.sources.split(',')
    input_dir = args.input_dir
    output_dir = args.output_dir
    model = args.model
    device = args.device

    dh.process_directory(input_dir, sources, model, device, output_dir)
    
if __name__ == "__main__":
    parse_and_process()
