from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from src.api import router as api_router
from src.core.create_superuser import create_superuser

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",  # имя контейнера из docker-compose
    agent_port=6831,
)

# Настройка провайдера и процессора
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "fastapi-service"})
    )
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)


@asynccontextmanager
async def lifespan(main_app: FastAPI):
    try:
        await create_superuser()
    except Exception as e:
        print(e)
    yield

app = FastAPI(
    lifespan=lifespan,
)
FastAPIInstrumentor.instrument_app(app)
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("src.app:app", host="localhost", port=8080, reload=True)
