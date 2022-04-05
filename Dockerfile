FROM public.ecr.aws/lambda/python:3.8

RUN yum -y install gcc-c++ pkgconfig poppler-cpp-devel poppler-utils python-devel redhat-rpm-config

RUN pip install -U pip-tools && \
pip install -U pdftotext

COPY . .

RUN pip install -r requirements.txt

CMD ["src.core.pdf_extractor.lambda_handler"]