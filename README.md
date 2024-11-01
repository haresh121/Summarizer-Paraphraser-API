# Summarization & Praphrasing API

--------------------------------

To run the files in the docker environment please use the following command
```python
docker-compose up -d # To run in detached mode
```

Send a POST request to the localhost:8002/summarize with the following JSON Payload
```json
{
    "text": "<text to summarize>"
}
```

Send a POST request to the localhost:8002/paraphrase with the following JSON Payload
```json
{
    "text": "<text to paraphrase>",
    "n": <number of sequences to generate>
}
```

To check the health of the API, send a GET request to the `localhost:8002/health`