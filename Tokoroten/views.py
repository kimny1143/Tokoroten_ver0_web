import os
import shutil
from django.shortcuts import render, redirect
from .directory_handler import process_directory
from django.conf import settings

def index(request):
    if request.method == 'POST':
        files = request.FILES.getlist('file-input')  # Get the uploaded files
        sources = request.POST.getlist('sources')  # Get the sources

        output_files = []

        # Create a temporary directory for the uploaded files
        temp_dir = settings.MEDIA_ROOT
        os.makedirs(temp_dir, exist_ok=True)

        # Save all the uploaded files to the temporary directory
        for file in files:
            file_path = os.path.join(temp_dir, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        # Process all the files in the temporary directory
        process_directory(temp_dir, sources, 'umxl', 'cpu', temp_dir)

        # Get the processed files
        for source in sources:
            output_filename = f"{os.path.splitext(file.name)[0]}_{source}.wav"
            output_path = os.path.join(temp_dir, output_filename)
            relative_output_path = os.path.relpath(output_path, settings.MEDIA_ROOT)  # Get the relative path
            output_files.append(relative_output_path)

        # Pass the processed files to the template
        return render(request, 'index.html', {'output_files': output_files})

    return render(request, 'index.html')

def delete_files(request):
    media_dir = settings.MEDIA_ROOT
    for filename in os.listdir(media_dir):
        file_path = os.path.join(media_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    return redirect('index')  # Redirect to index view
