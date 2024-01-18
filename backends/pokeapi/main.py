import logging
import os
from fastapi import FastAPI
from requests import HTTPError
from otel import instrument_application
from client import get_pokemon_by_name
import uvicorn

SERVICE_NAME = os.environ.get("SERVICE_NAME", "pokeapi")
GRPC_RECEIVER_ENDPOINT = os.environ.get("GRPC_RECEIVER_ENDPOINT", "otel-collector:4317")

app = FastAPI()

logger = logging.getLogger("pokeapi")


@app.get("/pokemon/{name}")
def get_pokemon(name: str):
    try:
        pokemon = get_pokemon_by_name(name)
        logger.info(f"Found pokemon in external api with name {name}")
        return pokemon
    except HTTPError as e:
        logger.error(f"Failed to get pokemon {name}: {e}")
        raise e


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)


instrument_application(
    application=app,
    service_name=SERVICE_NAME,
    grpc_receiver_endpoint=GRPC_RECEIVER_ENDPOINT,
)
