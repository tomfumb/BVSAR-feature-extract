#!/bin/sh

DCO_COMMON="docker-compose -f docker-compose.yml -f docker-compose.test.yml"

${DCO_COMMON} build --progress=plain
${DCO_COMMON} run api poetry run pytest
