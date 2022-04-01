# <img src="https://github.com/will-afs/PDFExtractor/blob/main/doc/img/pickaxe.png" width="30"> PDFExtractor
Extract data from scientific articles (PDF)

<img src="https://github.com/will-afs/PDFExtractor/blob/main/doc/img/PDFExtractor%20architecture.JPG" width="700">

This is a sub-project of the [AdvancedAcademicProject](https://github.com/will-afs/AdvancedAcademicProject/)

⚙️ Configuration
-----------------
The project configuration holds in the [settings/config.toml file](https://github.com/will-afs/PDFExtractor/blob/main/settings/config.toml)

Please check the 'cooldown_manager_uri' in it is correct, so that the Cooldown Manager can be reached

🐇 Quickly run the service as a container
------------------------------------------

    sudo docker run -p 9000:8080 williamafonso/pdfextractor:latest
    
By default, the entrypoint of the function will be: http://localhost:9000/2015-03-31/functions/function/invocations

So you can request it locally, for instance from a terminal:

    curl -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" -d "{\"uri\":\"http://arxiv.org/pdf/cs/9308101v1\",\"title\":\"DynamicBacktracking\",\"authors\":[\"M.L.Ginsberg\"]}"

You should obtain the following answer:

🧪 Developing and running tests
--------------------------------
In a terminal, run the following command:

    git clone https://github.com/will-afs/PDFExtractor.git

For the following, the working directory will be the root of this folder:

    cd PDFExtractor/
    
Add the working directory to the Python PATH environment variable:

    export PYTHONPATH=$(pwd)
    
Create a virtual environment:

    python3 -m venv .venv

Activate the virtual environment:
    
    source .venv/bin/activate
    
Install the dependencies:
    
    pip install -r requirements.txt

Run the main python file:

    python src.core.pdf_extractor.py

The tests are placed in the tests folder. They can be ran with pytests, as follows:

    python -m pytest tests

 🐋 Containerizing the application 
----------------------------------
To build a Docker image :

    sudo docker build --tag pdfextractor .
    
Or if you want to be able to push it to your DockerHub:

    sudo docker build --tag <your_docker_username>/pdfextractor .

Pushing the Docker image to your registry :

    sudo docker push <your_docker_user_name>/pdfextractor

You can now run the Docker image as a container :

    sudo docker run -d -p 80:80 pdfextractor
