FROM python:3.10

# Set environment variables for Qt
ENV DISPLAY=:99
ENV QT_QPA_PLATFORM=xcb

# Install system dependencies
RUN apt-get update && apt-get install -y \
    x11-xserver-utils \
    xauth \
    xvfb \
    libxkbcommon-x11-0 \
    libegl1-mesa \
    && rm -rf /var/lib/apt/lists/*

# RUN apt-get update && \
#     apt-get install -y \
#     build-essential \
#     libx11-dev \
#     libxext-dev \
#     libxrender-dev \
#     libfreetype6-dev \
#     libqt6core6 \
#     libqt6widgets6 \
#     xvfb \
#     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR /tests/ 

# CMD ["sh", "-c", "xvfb-run --auto-servernum pytest --md ./test-reports/report.md -v"]
# CMD ["xvfb-run" "-a", "pytest", "--md", "./test-reports/report.md", "-v"]
CMD ["sh", "-c", "Xvfb :99 -screen 0 1024x768x16 & pytest --md ./test-reports/report.md -v"]