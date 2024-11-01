from time import process_time
from flask import Flask, jsonify, request
from transformers import pipeline
from transformers import BartForConditionalGeneration, BartTokenizer

app = Flask(__name__)

summarizer = pipeline("summarization", model="pszemraj/led-base-book-summary")
paraphraser = BartForConditionalGeneration.from_pretrained(
    "eugenesiow/bart-paraphrase"
)
tokenizer = BartTokenizer.from_pretrained("eugenesiow/bart-paraphrase")


@app.get("/health")
def test():
    return jsonify({"status": "Working"})


@app.post("/summarize")
def summarize():
    start_time = process_time()

    try:
        data = request.get_json()

        text = data["text"]

        summary = summarizer(
            text,
            min_length=8,
            max_length=256,
            num_beams=4,
            do_sample=False,
            early_stopping=True,
        )[0]["summary_text"]

    except Exception as e:
        return jsonify(status=500, info="Internal Server Error", e=e)

    end_time = process_time()
    time_taken = end_time - start_time

    return jsonify(summary=summary, time=time_taken)


@app.post("/paraphrase")
def paraphrase():
    start_time = process_time()

    try:
        data = request.get_json()

        text = data["text"]
        n = data["n"]

        batch = tokenizer(text, return_tensors="pt")
        ids = paraphraser.generate(
            batch["input_ids"],
            num_beams=4,
            num_return_sequences=n,
            early_stopping=True,
        )
        paraphrases = tokenizer.batch_decode(ids, skip_special_tokens=True)

    except Exception as e:
        return jsonify(status=500, info="Internal Server Error", e=e)

    end_time = process_time()
    time_taken = end_time - start_time

    return jsonify(paraphrases=paraphrases, time=time_taken)


if __name__ == "__main__":
    app.run("localhost", 4304, debug=True)
