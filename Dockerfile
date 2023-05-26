FROM python:3
EXPOSE 8055
ENV PYTHONDONTWRITEBYTECODE=1
# [UNSURE] Turns off buffering for easier container logging
# ENV PYTHONUNBUFFERED=1
COPY . .
RUN python -m pip install -r requirements.txt
VOLUME /mount
CMD ["sh", "run.sh"]
