FROM python:3.10

RUN pip install pyasn1

COPY vitals_data_models.py .
COPY data.csv .
COPY agent.py .

CMD ["python3", "agent.py"]

# to run this from the cli use:
# docker run --network=host [name]