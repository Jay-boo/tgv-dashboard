FROM python:3.7.2

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .
COPY ensai-2023-373710-216f5609f399.json .

RUN pip install --no-cache-dir -r  requirements.txt 
ENV PORT=8080

COPY main.py . 

CMD streamlit run main.py --server.port=${PORT}  --browser.serverAddress="0.0.0.0"
