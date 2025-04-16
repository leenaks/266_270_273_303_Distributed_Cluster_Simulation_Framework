FROM python:3.9-slim-bookworm

WORKDIR /app

COPY node_simulator/node.py .

RUN pip install requests

CMD ["python", "node.py"]
