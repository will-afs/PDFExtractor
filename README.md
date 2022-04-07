# <img src="https://github.com/will-afs/AdvancedAcademicProject/blob/main/doc/Icons/PDFExtractor.png" width="30"> PDFExtractor
Extract data from scientific articles (PDF)

<img src="https://github.com/will-afs/AdvancedAcademicProject/blob/main/doc/Deployment%20architecture/PDFExtractor/PDFExtractor%20architecture.png" width="700">

This is a sub-project of the [AdvancedAcademicProject](https://github.com/will-afs/AdvancedAcademicProject/)

⚙️ Configuration
-----------------
The project configuration holds in the [settings/config.toml file](https://github.com/will-afs/PDFExtractor/blob/main/settings/config.toml)

🐇 Quickly run the service as a container
------------------------------------------

    sudo docker run -p 9000:8080 williamafonso/pdfextractor:latest
    
By default, the entrypoint of the function will be: http://localhost:9000/2015-03-31/functions/function/invocations

So you can request it locally, for instance from a terminal:

    curl -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" -d "{\"uri\":\"http://arxiv.org/pdf/cs/9308101v1\",\"title\":\"DynamicBacktracking\",\"authors\":[\"M.L.Ginsberg\"]}"

You should obtain the following answer:

    {"status": 200, "headers": {"Content-Type": "application/json"}, "message": "Success", "body": {"uri": "http://arxiv.org/pdf/cs/9308101v1", "authors": ["M.L.Ginsberg"], "title": "DynamicBacktracking", "references": [{"authors": ["Bruynooghe, M."]}, {"authors": ["Information Processing Letters, 12(1), 36{39. de Kleer, J."]}, {"authors": ["Information Processing Letters, 12(1), 36{39. de Kleer, J."]}, {"authors": ["Dechter, R.", "Meiri, I."]}, {"authors": ["Gaschnig, J."]}, {"authors": ["Ginsberg, M. L.", "Frank, M.", "Halpin, M. P.", "Torrance, M. C."]}, {"authors": ["Ginsberg, M. L.", "Harvey, W. D."]}, {"authors": ["Jonsson, A. K.", "Ginsberg, M. L."]}, {"authors": ["McAllester, D. A."]}, {"authors": ["Minton, S.", "Johnston, M. D.", "Philips, A. B.", "Laird, P."]}, {"authors": ["P. Purdom, C. B.", "Robertson, E."]}, {"authors": ["Seidel, R."]}, {"authors": ["Selman, B.", "Levesque, H.", "Mitchell, D."]}, {"authors": ["Smith, D. E.", "Genesereth, M. R."]}, {"authors": ["Stallman, R. M.", "Sussman, G. J."]}, {"authors": ["Zabih, R."]}, {"authors": ["Zabih, R.", "McAllester, D. A."]}]}}

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

You can now run the Docker image locally as a container :

    sudo docker run -p 9000:8080 pdfextractor:latest
    
☁️ Deploying on AWS Lambda
---------------------------
Connect to AWS via your web browser

Create a Container Registry for this project, and retrieve its URI and region. For example:

    849663779938.dkr.ecr.eu-west-3.amazonaws.com/pdfextractor:latest
    eu-west-3

From your CLI, make sure your AWS CLI is correctly configured (sudo is needed here if you need to run the following commands as sudo):

    sudo aws configure

Retrieve an AWS authentication token and authenticate your Docker client to your registry:

    sudo aws ecr get-login-password --region <your_region> | sudo docker login --username AWS --password-stdin <your_ecr_uri>

Make sure you have build a Docker image for the application (see how above)

After the build is complete, tag your image so you can push the image to your AWS ECR:

    sudo docker tag <your_docker_username>/pdfextractor:latest <your_ecr_uri>

Push your docker image to your AWS ECR. Example:

    sudo docker push <your_ecr_uri>/pdfextractor:latest
    
Create an AWS Lambda function, selecting Lambda from "image"

Add a VPC to AWS Lambda to enable it communicating with other applications from within (ArXivParser).
You might need to edit the Lambda-role by adding a new policy (e.g. AmazonEC2FullAccess).

Now test it with the following request body:

    {
        "uri": "http://arxiv.org/pdf/cs/9308102v1",
        "title": "Dynamic Backtracking",
        "authors": [
            "M. L. Ginsberg"
        ]
    }

Create a trigger:
- "API Gateway"
- API: "Create an API"
- API type: "REST API"
- Security: "Open"
- Create a new role 'BasicLambdaRole'

Once the trigger is created, select it, create a POST method for this ressource, and deploy the API

If Lambda integration is selected, unselect it

You should now be able to test the API from the AWS console (use the request body provided above)

Now, deploy the API

And configure the Security Group attached to the VPC so that the API can be reached from the internet

Create an API key and bind it to the API Gateway so that the API can only be accessed by clients in possession of the key

You should now be able to test the API from a CLI. For example:

    curl -H "apikey: <your_api_key>" -X POST "<your_api_gateway_uri>" -d "{\"uri\":\"http://arxiv.org/pdf/cs/9308101v1\",\"title\":\"DynamicBacktracking\",\"authors\":[\"M.L.Ginsberg\"]}"
