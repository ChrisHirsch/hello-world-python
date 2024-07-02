FROM python:3.12-slim as build
WORKDIR /app
COPY *.py /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt -t /app

#RUN python -m venv /src/venv
#RUN pwd
#RUN pip install -r /src/requirements.txt

#COPY --chown=python:python --from=build /src/venv /app

FROM python:3.12-slim
RUN useradd -m python
WORKDIR /app
COPY --from=build /app /app
#COPY --from=build /app/*.py /app
RUN ls -laR /app
RUN chown -R python:python /app
USER python
EXPOSE 8080
#ENV NAME World
#ENV PATH="/app/venv/bin:$PATH"
CMD ["python", "hello-world.py"]

