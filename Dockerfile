FROM python:3.11-slim
COPY . /summarization_and_paraphraser_api
WORKDIR /summarization_and_paraphraser_api
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends libgl1-mesa-glx libglib2.0-0 && apt-get -y install gcc python3-dev
RUN pip install -r requirements.txt
RUN pip install gunicorn
EXPOSE 8001
ENV FLASK_APP app.py