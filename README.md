# Simulador de Dispositivos e Medições - FastAPI

Este projeto é uma API desenvolvida com **FastAPI** para simular dispositivos e medições. Ele fornece endpoints para gerenciar dispositivos, obter medições e monitorar o status do servidor.

## Requisitos

- **Python 3.9+**
- **Docker** (opcional, para execução em container)
- **pip** para gerenciar dependências

## Instalação

### Sem Docker

1. Clone o repositório:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DO_REPOSITORIO>
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o servidor:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

5. Acesse a documentação interativa da API:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Com Docker

1. Certifique-se de que o Docker está instalado e em execução.

2. Construa a imagem Docker:
   ```bash
   docker build -t simulador-fastapi .
   ```

3. Execute o container:
   ```bash
   docker run -p 8000:8000 simulador-fastapi
   ```

4. Acesse a API em [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Estrutura do Projeto

- `main.py`: Contém a lógica principal da API.
- `requirements.txt`: Lista de dependências do projeto.
- `Dockerfile`: Configuração para criar a imagem Docker.
- `build-mac.sh` e `build-linux.sh`: Scripts para construir e publicar imagens Docker para diferentes plataformas.

## Endpoints

### Status do Servidor
- **GET /api/status**: Retorna o status atual do servidor.
- **PUT /api/status**: Atualiza o status do servidor.

### Dispositivos
- **GET /api/devices**: Retorna todos os dispositivos.
- **GET /api/devices/{hnuid}**: Retorna informações de um dispositivo específico.
- **PUT /api/devices/{hnuid}/zero**: Reseta as medições de um dispositivo.

### Medições
- **GET /api/devices/{hnuid}/measurements**: Retorna medições de um dispositivo.
- **PUT /api/devices/measurements**: Atualiza medições (simulado).

## Exemplos de Uso

### Obter Status do Servidor
```bash
curl -X GET http://127.0.0.1:8000/api/status
```

### Atualizar Status do Servidor
```bash
curl -X PUT "http://127.0.0.1:8000/api/status?isRunning=false&consoleVisible=false"
```

### Obter Dispositivos
```bash
curl -X GET http://127.0.0.1:8000/api/devices
```

### Obter Medições de um Dispositivo
```bash
curl -X GET "http://127.0.0.1:8000/api/devices/201-001-40/measurements?qtd=5"
```

## Scripts de Build

- **`build-mac.sh`**: Constrói e publica a imagem Docker para a plataforma `linux/arm64`.
- **`build-linux.sh`**: Constrói e publica a imagem Docker para a plataforma `linux/amd64`.

## Tecnologias Utilizadas

- **FastAPI**: Framework para construção de APIs rápidas e eficientes.
- **Pydantic**: Validação de dados e criação de modelos.
- **Docker**: Containerização da aplicação.

## Contribuição

1. Faça um fork do repositório.
2. Crie uma branch para sua feature ou correção:
   ```bash
   git checkout -b minha-feature
   ```
3. Faça commit das suas alterações:
   ```bash
   git commit -m "Minha nova feature"
   ```
4. Envie para o repositório remoto:
   ```bash
   git push origin minha-feature
   ```
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
