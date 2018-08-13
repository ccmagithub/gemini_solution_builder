FROM alpine:latest

RUN apk add --update \
    python \
    python-dev \
    py-pip \
    && mkdir gemini_solution_builder

WORKDIR gemini_solution_builder/

COPY ./ ./

RUN pip install -r requirements.txt \
    && pip install -e .

VOLUME example/

CMD gsb
