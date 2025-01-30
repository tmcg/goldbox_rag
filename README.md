
### Python Virtual Environment

# Creation
mkdir venv
python -m venv ./venv

# Activation (via Powershell)
./venv/scripts/activate.ps1
pip install -r ./requirements.txt


### Crawling Topic page URLs

```
> python ./goldbox_crawl.py
> streamlit run ./goldbox_agent_ui.py
```

NOTE: mistral and llama3.2 generate different size vector embeddings to the original openAI sample code
mistral = 4096, llama3.2 = 3072



### Running a model locally with Ollama

```
> ollama pull llama3.2
pulling manifest...
writing manifest...
success

> ollama list
NAME                ID              SIZE      MODIFIED
llama3.2:latest     a80c4f17acd5    2.0 GB    12 minutes ago
mistral:latest      f974a74358d6    4.1 GB    22 hours ago
deepseek-r1:8b      28f8fd6cdc67    4.9 GB    2 days ago
deepseek-r1:1.5b    a42b25d8c10a    1.1 GB    2 days ago
```

### Show model information

```
> ollama show mistral
  Model
    architecture        llama
    parameters          7.2B
    context length      32768
    embedding length    4096
    quantization        Q4_0
 ...

> ollama show llama3.2
  Model
    architecture        llama
    parameters          3.2B
    context length      131072
    embedding length    3072
    quantization        Q4_K_M
  ...
```


### Starting Ollama

- Launch via CLI, with "ollama serve" -OR-
- Launch via the start menu, Ollama creates a tray icon


### Querying the Ollama endpoint directly

curl -X POST http://localhost:11434/api/generate `
    -d '{"model": "mistral", "prompt": "Tell me a joke about llamas"}'
