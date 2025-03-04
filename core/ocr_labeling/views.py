from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os

from .index import run_ocr, run_ollama

# Create your views here.
class OCRLabelingView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the directory exists
        upload_dir = "uploads/"
        os.makedirs(upload_dir, exist_ok=True)

        # Save the file temporarily
        save_path = f"uploads/{file.name}"
        with open(save_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        try:
            ocr_text = run_ocr(save_path)
            ollama_output = run_ollama(ocr_text)
            return Response({
                "ocr_text": ocr_text,
                # "ollama_output": ollama_output,
                "file_path": save_path
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Cleanup on failure
            if os.path.exists(save_path):
                os.remove(save_path)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        


class OCRLabelingBatchView(APIView):
    def post(self, request):
        files = request.FILES.getlist('files')  # Get all files uploaded with the 'files' key
        if not files:
            return Response({"error": "No files provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the upload directory exists
        upload_dir = "bulk/"
        os.makedirs(upload_dir, exist_ok=True)

        results = []

        for file in files:
            save_path = os.path.join(upload_dir, file.name)
            
            # Save the file temporarily
            with open(save_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)

            try:
                # Run OCR and any other processing
                ocr_text = run_ocr(save_path)
                ollama_output = run_ollama(ocr_text)

                # Append the result for this file
                results.append({
                    "file_name": file.name,
                    "ocr_text": ocr_text,
                    "file_path": save_path
                })

            except Exception as e:
                # Handle errors for individual files
                results.append({
                    "file_name": file.name,
                    "error": str(e)
                })
            
            finally:
                # Cleanup temporary file
                if os.path.exists(save_path):
                    os.remove(save_path)

        return Response({"results": results}, status=status.HTTP_200_OK)