FROM python:3.6.11-stretch
COPY ./services /services
WORKDIR /services
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && chmod +x /services/entrypoint.sh
EXPOSE 8000
CMD ["/services/entrypoint.sh"]