from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import time
from zipfile import ZipFile

from .serializers import BulkUploadSerializer, DocumentClassifierSerializer
from .ml.classify import classify_document, preprocess_document


# def process_single_document(file_path):
#     classifier_result = run_classifier(file_path)  # Call your classifier
#     ocr_result = run_ocr(file_path)  # Call your OCR module
#     expected_type = get_expected_type(file_path)  # Application context

#     is_valid_type = classifier_result['class'] == expected_type
#     is_valid_data = validate_extracted_data(ocr_result, expected_type)

#     return {
#         "file_name": os.path.basename(file_path),
#         "classification": classifier_result,
#         "ocr_data": ocr_result,
#         "is_valid_type": is_valid_type,
#         "is_valid_data": is_valid_data
#     }
class DocumentClassifierView(APIView):
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
            document_class, confidence_score = classify_document(save_path)
            return Response({
                "class": document_class,
                "confidence_score": confidence_score,
                "file_path": save_path
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Cleanup on failure
            if os.path.exists(save_path):
                os.remove(save_path)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BulkVerifyViewZip(APIView):
    def post(self, request):
        start_time = time.time()
        zip_file = request.FILES.get('bulk_file')
        
        if not zip_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = DocumentClassifierSerializer(data={"file" :  zip_file})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        out_dir = "bulk/uploads" 
        os.makedirs(out_dir, exist_ok=True)
        zip_path = os.path.join(out_dir, zip_file.name)
        
        with open(zip_path, 'wb') as f:
            for chunk in zip_file.chunks():
                f.write(chunk)
            
        with ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(out_dir)
            
        files = [os.path.join(out_dir, file) for file in os.listdir(out_dir)]
        results = []
        
        for file_path in files:
            try:
                result = classify_document(file_path)
                results.append({file_path :result})
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}") 
                
        end_time = time.time()
        
        return Response({
            "processing_time": end_time - start_time,
            "total_documents": len(files),
            "result": results
        }, status=status.HTTP_200_OK)     
        

class BulkVerifyFileView(APIView):
      def post(self, request):
        start_time = time.time()
        
        # Get the uploaded files from the request
        uploaded_files = request.FILES.getlist('files')  # This will give you a list of files
        
        if not uploaded_files:
            return Response({"error": "No files provided"}, status=status.HTTP_400_BAD_REQUEST)

        results = []
        
        for file in uploaded_files:
            try:
                # Assuming classify_document is a function that processes the image
                class_name, confidence_score = classify_document(file)
                if float(confidence_score) < 0.75:
                    results.append({
                    "file_name": file.name,
                    "class": "Invalid",
                    "confidence_score": confidence_score
                })                        
                results.append({
                    "file_name": file.name,
                    "class": class_name,
                    "confidence_score": confidence_score
                })
            except Exception as e:
                results.append({
                    "file_name": file.name,
                    "error": str(e)
                })
        
        end_time = time.time()
        
        # Return the results with processing time
        return Response({
            "processing_time": end_time - start_time,
            "total_files": len(uploaded_files),
            "results": results
        }, status=status.HTTP_200_OK)