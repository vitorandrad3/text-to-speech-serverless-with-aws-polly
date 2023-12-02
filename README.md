# Conversor de texto para áudio (Text To Speech)

De modo geral, essa atividade foi desenvolvida para converter um texto enviado pelo usuário em um arquivo de áudio.

##  Índice: <a name="ancora"></a>

1. [Desenvolvimento do Projeto](#desenvolvimento-do-projeto)
2. [Estrutura de pastas](#estrutura-de-pastas)
3. [Funcionalidades](#funcionalidades)
4. [Acesso ao sistema](#acesso_ao_sistema)
5. [Como utilizar a aplicação](#como-utilizar)
6. [Arquitetura do projeto](#arquitetura-do-projeto)
7. [Testes de unidade](#testes-de-unidade)

## Desenvolvimento do projeto <a name="desenvolvimento-do-projeto"></a>

As tecnologias utilizadas para a criação do projeto incluem o framework ***Serverless*** e a linguagem ***Python***.  
Primeiramente, foi necessário configurar as credenciais do usuário IAM criado para essa aplicação em específico. A configuração das credenciais garante que o usuário acesse os serviços da amazon utilizados no nosso projeto, tais como: ***Polly***, ***DynamoDB***, ***S3*** e ***Lambda***.  
Em segundo lugar, foi o desenvolvimento do projeto em si, ou seja,  a criação dos *handlers* para cada serviço definido no escopo da atividade (v1/tts, v2/tts e v3/tts).  
Por último, foi incorporado ao projeto um conjunto de testes para trazer maior qualidade ao código e, para isso, foram utilizadas as bibliotecas *pytest* e *unittest*.  

## Estrutura de pastas <a name="estrutura-de-pastas"></a>
Escolhemos uma estrutura de pastas com base no que foi oferecido pela documentação do framework ***Serverless***. 
- Na pasta `aws` fizemos a configuração do *boto session* e dos *clients* de cada serviços da AWS. 
- Na pasta `services` possui os *handlers* de cada rota da aplicação.
- Na pasta `tests` está o conjunto de testes automatizados
- Na pasta `utils` estão algumas funções para o funcionamento do programa

```shell
├─ src/
│   	├─ aws/
│	│	├─ dynamo/
│	│	│	└─ dynamo_client.py
│	│	│	├─ functions/
│	│	│		└─ fetch_on_dynamo.py
│	│	│		└─ save_on_dynamo.py
│	│	│	
│	│	├─ polly/
│	│	│	└─ polly_client.py
│	│	│	├─ functions/
│	│	│		└─ text_to_speech.py
│	│	│
│	│	├─ s3/
│	│	│	└─ s3_client.py
│	│	│	├─ functions/
│	│	│		└─ save_audio_on_s3
│	│	└─ boto_session.py
│	│	
│	├─ services/
│	│	├─ template/
│	│	│	└─ handler.py
│	│	├─ v1_tts/
│	│	│	└─ handler.py
│	│	├─ v2_tts/
│	│	│	└─ handler.py
│	│	├─ v3_tts/
│	│		└─ handler.py
│	│	
│	├─ tests/
│	│
│	├─ utils/
│		└─ format_date.py
│		└─ hash_generator.py
│		├─ error_class/
│			└─ api_error_class.py
│
├─ .env.example
├─ .gitignore
├─ __init__.py
├─ package.json
├─ requirements.txt
├─ serverless.yml
├─ setup.py
```

## Funcionalidades: <a name="funcionalidades"></a>
Ao enviar via método POST um JSON seguindo o formato abaixo:  
```json
{
	"phrase": "<substituir pela frase desejada>"
}
```
O programa retornará a frase enviada pelo cliente, uma URL para acessar o áudio criado e a data de criação do arquivo de áudio. Vale lembrar que o retorno muda de acordo com a rota em que o cliente está realizando a requisição.

## Acesso ao sistema: <a name="acesso_ao_sistema"></a>

#### *** os endpoints estão atualmente inativos, estes são apenas de exemplos ***

### Rota -> Get `/`
```url
https://wgxznihk57.execute-api.us-east-1.amazonaws.com/
```
### Rota -> POST `/v1/tts`
```url
https://wgxznihk57.execute-api.us-east-1.amazonaws.com/v1/tts
```
### Rota -> POST `/v2/tts`
```url
https://wgxznihk57.execute-api.us-east-1.amazonaws.com/v2/tts
```
### Rota -> POST `/v3/tts`
```url
https://wgxznihk57.execute-api.us-east-1.amazonaws.com/v3/tts
```
## Como utilizar a aplicação: <a name="como-utilizar"></a>
Acessar os links de cada rota [/v1/tts], [/v2/tts] ou [/v3/tts] utilizando um software de envio de requisições (exemplo: *Postman*) fornecendo os modelos *post* listados abaixo:

### [/v1/tts](https://wgxznihk57.execute-api.us-east-1.amazonaws.com/v1/tts)
post:
```json
{
    "phrase": "testando a rota v1 texto para audio "
}
```
resposta:
```json
{ 
    "received_phrase": "testando a rota v1 texto para audio ",
    "url_to_audio": "s3_audio_link_exemple.com",
    "created_audio": "27-09-2023 19:38:40"
}
```
### [/v2/tts](https://wgxznihk57.execute-api.us-east-1.amazonaws.com/v2/tts)
post:
```json
{
    "phrase": "testando a rota v2 texto para audio"
}
```
resposta:
```json
{
    "received_phrase": "testando a rota v2 texto para audio",
    "url_to_audio":"s3_audio_link_exemple.com",
    "created_audio": "27-09-2023 23:02:30",
    "unique_id": "fdbc9d9e3039f80b6710e41ac6305fe0"
}
```
### [/v3/tts](https://wgxznihk57.execute-api.us-east-1.amazonaws.com/v3/tts)
post:
```json
{
    "phrase": "testando a rota v3 texto para audio"
}
```
resposta:
```json
{
    "received_phrase": "testando a rota v3 texto para audio",
    "url_to_audio": "s3_audio_link_exemple.com",
    "created_audio": "27-09-2023 19:50:25",
    "unique_id": "231e22bee38eb577fe646f905a2f2426"
}
```

## Arquitetura do projeto: <a name="arquitetura-do-projeto"></a>
A arquitetura do projeto é dividia em cada endpoint gerado pelo deploy da aplicação

### Rota /v1/tts:
![arquitetura_v1](https://github.com/Compass-pb-aws-2023-FATEC/sprint-6-pb-aws-fatec/assets/93358971/f217111d-3800-40bc-aa6c-0d6e1a86d959)

### Rota /v2/tts
![arquitetura_v2](https://github.com/Compass-pb-aws-2023-FATEC/sprint-6-pb-aws-fatec/assets/93358971/8f287157-3650-4e37-82c0-cd2537e5c28a)


### Rota /v3/tts
![arquitetura_v3](https://github.com/Compass-pb-aws-2023-FATEC/sprint-6-pb-aws-fatec/assets/93358971/d3d14647-d55e-4489-8b18-1e9deeaedba2)

## Testes de unidade <a name="testes-de-unidade"></a>
Foram elaborados testes de unidade no nosso projeto usando a biblioteca ***pytest***, visando elevar a qualidade do código desenvolvido. Os testes apresentaram um *coverage* de 96%.

![pytest_coverage](https://github.com/Compass-pb-aws-2023-FATEC/sprint-6-pb-aws-fatec/assets/93358971/15a3d408-9a83-4211-b1b0-04751c93cd57)
