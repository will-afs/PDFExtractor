# <img src="" width="30"> PDFExtractor
Extract data from scientific articles (PDF)

<img src="" width="700">

This is a sub-project of the [AdvancedAcademicProject](https://github.com/will-afs/AdvancedAcademicProject/)

⚙️ Configuration
-----------------
The project configuration holds in the settings/config.toml file.
Please check the 'cooldown_manager_uri' in it is correct.

🔽 Installing the project on your machine
------------------------------------------
In a terminal, run the following command :

    git clone https://github.com/will-afs/PDFExtractor.git

For the following, the working directory will be the root of this folder :

    cd PDFExtractor/
    
Build a Docker image :

    sudo docker build --tag pdfextractor .

▶️ Usage
---------
You can now run the Docker image as a container :

    sudo docker build --tag pdfextractor .

By default, the entrypoint of the function to embed in AWS-Lambda will be : http://localhost:9000/2015-03-31/functions/function/invocations

You can request it locally, for instance from a terminal :

    curl -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" -d "{\"uri\":\"http://arxiv.org/pdf/cs/9308101v1\",\"title\":\"DynamicBacktracking\",\"authors\":[\"M.L.Ginsberg\"]}"

You should obtain the following answer :


(optionnal) You can also push the Docker image to your own registry :

    sudo docker push <your_docker_user_name>/pdfextractor
    
🧪 Running tests
-----------------
The tests are placed in the tests folder. They can be ran with pytests, as follows :

    export PYTHONPATH=$(pwd)
    python -m pytest tests
