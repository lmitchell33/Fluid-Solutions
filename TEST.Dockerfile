FROM python:3

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD ["/bin/bash", "pytest", "tests/", "--md", "report.md", "-v"]