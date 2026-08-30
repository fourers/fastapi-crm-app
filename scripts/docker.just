image_name := "fastapi-crm-app"

[no-cd]
build:
    docker build . -t {{ image_name }}

run:
    docker run --rm -it -p 8000:8000 {{ image_name }}

shell_docker:
    docker run --rm -it --entrypoint bash {{ image_name }}
