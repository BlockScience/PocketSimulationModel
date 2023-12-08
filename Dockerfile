FROM continuumio/miniconda3:4.11.0
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY model model
COPY data data
COPY cloud_run.py .
ENTRYPOINT ["python", "cloud_run.py"]