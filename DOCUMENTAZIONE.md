# Documentazione del progetto
## Deploy e monitoraggio di un modello di Sentiment Analysis per recensioni

### 1. Descrizione del progetto

Il progetto realizza un servizio di **Sentiment Analysis** per classificare recensioni testuali e integra il modello in una API web Flask.

L'obiettivo è costruire una soluzione completa che comprenda:

- modello di Machine Learning per la classificazione del sentiment;
- API REST per effettuare le predizioni;
- test automatici con pytest;
- containerizzazione con Docker;
- pipeline CI/CD con Jenkins;
- versionamento del codice tramite GitHub;
- avvio automatico della pipeline tramite GitHub Webhook;
- monitoraggio tramite Prometheus;
- dashboard di monitoraggio tramite Grafana.

Il progetto è stato verificato eseguendo realmente la pipeline Jenkins e ottenendo una conclusione `Finished: SUCCESS`.

---

## 2. Tecnologie utilizzate

- **Python 3.13**
- **Flask**
- **scikit-learn 1.6.0**
- **CountVectorizer**
- **MultinomialNB**
- **pytest**
- **Docker**
- **Jenkins**
- **Git / GitHub**
- **Ngrok** per rendere raggiungibile Jenkins locale dal webhook GitHub
- **Prometheus**
- **Grafana**
- **psutil**
- **prometheus-client**

La versione `scikit-learn==1.6.0` è fissata nel file `requirements.txt` per mantenere la compatibilità con il modello serializzato tramite pickle.

---

## 3. Struttura del progetto

```text
sentiment-analysis-devops/
│
├── app/
│   ├── app.py
│   └── model/
│       └── sentiment_analysis_model.pkl
│
├── tests/
│   ├── test_api.py
│   └── test_model.py
│
├── prometheus/
│   └── prometheus.yml
│
├── Dockerfile
├── Dockerfile.jenkins
├── docker-compose.yml
├── Jenkinsfile
├── pytest.ini
├── requirements.txt
├── .dockerignore
├── .gitignore
├── README.md
└── test_model.py
```



---

## 4. Modello di Sentiment Analysis

Il modello utilizzato è un modello scikit-learn serializzato nel file:

```text
app/model/sentiment_analysis_model.pkl
```

Il modello è una pipeline composta da:

```text
CountVectorizer
      ↓
MultinomialNB
```

Le tre classi di sentiment gestite sono:

```text
positive
negative
neutral
```

L'applicazione utilizza anche `predict_proba()` per ottenere la probabilità associata alla classe prevista e restituirla come valore di confidence.

---

## 5. API Flask

L'applicazione è implementata in:

```text
app/app.py
```

Il servizio Flask viene avviato sulla porta:

```text
5000
```

e ascolta su:

```text
0.0.0.0
```

### Endpoint `/`

Metodo:

```text
GET /
```

Viene utilizzato come endpoint di controllo e restituisce lo stato del servizio.

Esempio:

```json
{
  "service": "Sentiment Analysis API",
  "status": "running"
}
```

### Endpoint `/predict`

Metodo:

```text
POST /predict
```

Riceve un JSON contenente una recensione.

Esempio:

```json
{
  "review": "This product is amazing! I love it."
}
```

La risposta contiene il sentiment e la confidence:

```json
{
  "sentiment": "positive",
  "confidence": 0.5683
}
```

L'endpoint controlla inoltre:

- presenza del campo `review`;
- tipo stringa del valore;
- eventuali errori durante la predizione.

In caso di dati non validi viene restituito HTTP `400`.

In caso di errore interno viene restituito HTTP `500`.

### Endpoint `/metrics`

Metodo:

```text
GET /metrics
```

Espone le metriche utilizzate da Prometheus.

Le principali metriche sono:

```text
prediction_requests_total
prediction_errors_total
prediction_response_time_seconds
system_cpu_usage_percent
system_memory_usage_percent
```

---

## 6. Test automatici

I test sono contenuti nella cartella:

```text
tests/
```

e sono configurati tramite:

```text
pytest.ini
```

Sono presenti test relativi a:

- endpoint principale `/`;
- predizione positiva;
- predizione negativa;
- predizione neutra;
- richiesta senza recensione;
- recensione con tipo non valido;
- endpoint `/metrics`;
- caricamento del modello;
- predizione del modello;
- probabilità delle classi.

### Risultato della verifica

La pipeline Jenkins ha eseguito:

```text
10 tests
```

con risultato:

```text
10 passed in 1.67s
```

Tutti i test sono quindi risultati positivi.

---

## 7. Docker

Il servizio API è containerizzato tramite `Dockerfile`.

L'immagine utilizza:

```text
python:3.13-slim
```

La porta esposta dal container è:

```text
5000
```

Il comando di avvio è:

```text
python app/app.py
```

L'immagine utilizzata dalla pipeline Jenkins viene denominata:

```text
sentiment-api:jenkins
```

---

## 8. Docker Compose

Il file:

```text
docker-compose.yml
```

definisce tre servizi principali:

### sentiment-api

API Flask del progetto.

Porta:

```text
5000
```

### prometheus

Sistema di raccolta delle metriche.

Porta:

```text
9090
```

### grafana

Dashboard per la visualizzazione delle metriche.

Porta:

```text
3000
```

I tre servizi comunicano attraverso la rete Docker:

```text
sentiment-network
```

---

## 9. Prometheus

La configurazione è contenuta in:

```text
prometheus/prometheus.yml
```

Prometheus effettua lo scraping dell'API ogni:

```text
5 secondi
```

Il target configurato è:

```text
sentiment-api:5000
```

e l'endpoint utilizzato è:

```text
/metrics
```

Durante la verifica del progetto sono state rilevate correttamente metriche quali:

```text
prediction_requests_total
prediction_errors_total
system_cpu_usage_percent
system_memory_usage_percent
prediction_response_time_seconds
```

---

## 10. Grafana

Grafana viene utilizzato per visualizzare le metriche raccolte da Prometheus.

È stata configurata una dashboard denominata:

```text
Sentiment Analysis Monitoring
```

La dashboard comprende cinque pannelli:

1. **Prediction Requests**
   - numero delle richieste di predizione;

2. **Prediction Errors**
   - numero degli errori di predizione;

3. **API Response Time**
   - tempo medio di risposta;

4. **CPU Usage**
   - utilizzo percentuale della CPU;

5. **Memory Usage**
   - utilizzo percentuale della memoria.

Durante la verifica sono stati visualizzati valori reali nelle dashboard, confermando il corretto collegamento tra API, Prometheus e Grafana.

---

## 11. Jenkins e CI/CD

La pipeline è definita nel file:

```text
Jenkinsfile
```

La pipeline contiene tre fasi principali.

### Stage 1 - Test

Jenkins installa le dipendenze definite in:

```text
requirements.txt
```

ed esegue:

```text
python3 -m pytest -v
```

La fase è stata verificata con:

```text
10 passed
```

### Stage 2 - Docker Build

Jenkins costruisce l'immagine:

```text
sentiment-api:jenkins
```

utilizzando:

```text
docker build -t sentiment-api:jenkins .
```

### Stage 3 - Deploy

Jenkins arresta ed elimina il container precedente e avvia il nuovo container:

```text
sentiment-api
```

utilizzando la nuova immagine.

La pipeline termina con:

```text
Pipeline completata con successo!
Finished: SUCCESS
```

---

## 12. Jenkins tramite Docker

Per eseguire Jenkins è stato utilizzato un'immagine personalizzata definita in:

```text
Dockerfile.jenkins
```

L'immagine comprende:

- Jenkins LTS;
- Docker CLI;
- Python 3;
- pip;
- virtual environment tools.

Jenkins comunica con il Docker Engine tramite il Docker socket, permettendo alla pipeline di costruire immagini e avviare container.

---

## 13. GitHub e versionamento

Il progetto è stato versionato tramite Git e pubblicato su GitHub.

Repository:

```text
https://github.com/Amosdev76/sentiment-analysis-devops
```

Il branch utilizzato è:

```text
main
```

Il Jenkins job utilizza:

```text
Pipeline script from SCM
```

e recupera il file:

```text
Jenkinsfile
```

direttamente dal repository GitHub.

---

## 14. GitHub Webhook e automazione

Per automatizzare l'avvio della pipeline è stato configurato un GitHub Webhook.

Il flusso è:

```text
git push
   ↓
GitHub
   ↓
GitHub Webhook
   ↓
Ngrok
   ↓
Jenkins
   ↓
Pipeline
```

Ngrok viene utilizzato perché Jenkins è eseguito localmente sulla macchina dello sviluppatore.

Il webhook è stato testato con successo.

Dopo una modifica al progetto e un:

```text
git push
```

GitHub ha inviato l'evento `push` a Jenkins e Jenkins ha avviato automaticamente una nuova build.

Questo ha verificato il funzionamento del processo CI/CD automatico.

---

## 15. Flusso completo del progetto

Il funzionamento complessivo può essere rappresentato come segue:

```text
Sviluppatore
     │
     │ git push
     ▼
   GitHub
     │
     │ Webhook
     ▼
   Ngrok
     │
     ▼
  Jenkins
     │
     ├── Test pytest
     │
     ├── Docker Build
     │
     └── Deploy
             │
             ▼
       Sentiment API
          /predict
          /metrics
             │
             ▼
         Prometheus
             │
             ▼
           Grafana
```

---

## 16. Verifica finale

La pipeline Jenkins è stata eseguita con successo.

Risultati verificati:

```text
Checkout GitHub          OK
Installazione dipendenze OK
Test pytest              10 passed
Docker Build             OK
Docker Deploy            OK
API Flask                OK
Prometheus               OK
Grafana                  OK
GitHub Webhook           OK
Pipeline Jenkins         SUCCESS
```

Il risultato finale della pipeline è stato:

```text
Finished: SUCCESS
```

---

## 17. Avvio manuale del progetto

Per avviare i servizi tramite Docker Compose:

```bash
docker compose up -d --build
```

Per verificare i container:

```bash
docker compose ps
```

L'API sarà disponibile sulla porta:

```text
http://localhost:5000
```

Prometheus:

```text
http://localhost:9090
```

Grafana:

```text
http://localhost:3000
```

Per arrestare i servizi:

```bash
docker compose down
```

---

## 18. Test dell'API

Un esempio di richiesta POST all'endpoint `/predict` è:

```json
{
  "review": "This product is amazing! I love it."
}
```

La risposta contiene:

```json
{
  "sentiment": "positive",
  "confidence": 0.5683
}
```

È inoltre possibile verificare le metriche tramite:

```text
http://localhost:5000/metrics
```

---

## 19. Conclusioni

Il progetto realizza una pipeline completa per il deploy e il monitoraggio di un modello di Sentiment Analysis.

La soluzione integra il modello di Machine Learning con una API Flask, test automatici, container Docker, pipeline Jenkins, versionamento GitHub, webhook automatico, raccolta metriche Prometheus e visualizzazione tramite Grafana.

La verifica finale ha dimostrato che un aggiornamento del repository può attivare automaticamente la pipeline Jenkins, che esegue i test, costruisce l'immagine Docker e aggiorna il servizio API.

Il progetto rispetta quindi il flusso operativo previsto:

```text
Commit → Test → Build → Deploy → Monitoraggio
```
