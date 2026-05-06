FROM python:3.12-slim

RUN apt-get update && apt-get install -y g++ python3-dev && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pybind11 setuptools

WORKDIR /app

COPY setup.py .
COPY backend/ backend/

WORKDIR /app/backend

RUN python3 ../setup.py build_ext --inplace

RUN pip install --no-cache-dir fastapi "uvicorn[standard]" pydantic

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
