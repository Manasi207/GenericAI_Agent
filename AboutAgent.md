## Public link (AWS Deployement)

### http://gen-ai-agent-bucket.s3-website.eu-north-1.amazonaws.com/

## Name

### Manasi Vijaykumar Sabale

## Agent Name as per the PDF

### Generic AI Agent ( Chrome Based Extension)

## Which LLM API are you using for generation?

### LLM API- OLLAMA_API_URL

### Other API- OPEN API KEY, OPENWEATHER API KEY

## What suggestion did Pritesh give you?

### In my case, when after user enters the website name, the agent is not able to directly access that site throught browser, it just gives a clickable link.

### Suggestion- To check log of why not browse through module not directly navigating to mentioned web application (NOW it is auto redirected to particular websites.

## What was the challenge you faced?

### Module takes time to generates response of havy modules such as Email sending & summarizing text. Latency in response of user entered prompt.

## Screenshot for your implementation.

### Drive link - https://drive.google.com/drive/folders/11pPIOOXEVSKHikM8LTyTdslbN4QV3ufK?usp=sharing

## Email Address

### manasi.official2024@gmail.com

## Give stepwise flow of what your agent does

### Once Chrome based extension loaded in browser. It will ready enter & hit send query( userentered).

### After that need to mention (text based )which module do you want to continue with, so add relavant keyword(add it initial)

### then modulewise work as per below mentioned:

#### Sentiment Analysis – Analyzes user-provided text and returns its sentiment (positive, negative, neutral) using the Ollama LLM.

#### Summarize Text – Takes long text input and returns a concise summary (short/medium/long) via LangChain prompts.

#### Send Mails – (need to mention recipient, subject, body)Sends emails through SMTP, optionally using templates and async background tasks for efficiency.

#### Weather – Fetches real-time weather data( evrything temperature, humidity, windflow) for a city or coordinates using the OpenWeather API.

#### Browse Website – Navigates to mentioned <website.com> URL.

## Tech-Stack Used-

### LLM API- OLLAMA_API_URL

### Other API- OPEN API KEY, OPENWEATHER API KEY

### Other Tools & Backend Technologies - Python, FastAPI(uvicorn Setting),Langchain, OLLAMA Local Server(with llama3 model), SMTP_PORT, SMTP_HOST

### Frontend Technologies- HTML, CSS, JS

## Github Profile

### https://github.com/Manasi207
