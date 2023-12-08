FROM continuumio/miniconda3:4.11.0
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY model .
COPY data .
COPY cloud_run.py .
ENTRYPOINT ["python", "cloud_run.py"]