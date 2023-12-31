# Hello API Service
- Documentation
- Prerequsites
- Testing
- Installation and Validation
- Notes & next steps

## Hello API Service Documentation
API Service uses Flask application and uvicorn web server for backend.
Swagger is added to simplify API endpoint management and documentation.

### Code structure
The API codebase is stored in **source** folder

Modules:
- api.hello is module which handle all API logic
- local_db is mock module to generate customers datastructure
- web_svc_functions is module which handles service functions required for API work

Tests:
 - source/tests/test_unit_api_hello.py - Basic unit tests
 - source/tests/test_functional_api_hello.py - Functional tests for Web Application

### API Endpoints
- /api/ui - Swagger UI which provides documentation for API endpoints
- /api/health - Basic Health check
- /api/hello - Greeting endpoint

### Swagger
Swagger library helps to simply organize API structure, keep and track API documenation as code.<br>
There is no needs for additional documantation/KB pages, because everything can be found in Swagger UI. The UI also allows to perform test API calls to real enpoints.<br>

Swagger confguration file - **source/modules/api/hello/swagger.yml**

### How to prepare Python venv
*cd source*<br>
*pip3 install venv*<br>
*python3.12 -m venv venv*<br>
*source venv/bin/activate*<br>
*pip3 install -r requirements.txt*

### How to run the API service
*cd source*<br>
*python3 app_hello_api.py*

## Prerequsites
Tools/modules below should be installed before run API service
python3
External Python modules:
 - Flask==3.0.0
 - connexion[swagger-ui,flask,uvicorn]==3.0.5
 - pytest==7.4.3

 All tests and development were performed with using **Python 3.12**, but it should work with any python3 distribution.

## Testing
Codebase contains unit and functional tests.

How to run tests:<br>
*cd source*<br>
*pytest*

## Installation and Validation
### Environment preparation
*All testing was performed under Macos*
1. Install brew
2. Install python3<br>
*brew install python@3.12*
3. Install modules<br>
*pip3 install -r requirements.txt*
4. Install docker<br>
*brew install docker*
5. Install minikube<br>
*brew install minikube*
6. Install kubectl<br>
*brew install kubectl*
7.Install yq<br>
*brew install yq*
8. Start docker
9. Start minikube: minikube start

### Manual validation
1. Set SERVICE_OWNER environment variable to specify greetings.
**local_db/db.py** contains all available owners
2. Start web server(it uses 8080 port by default)<br>
If needed you can set SERVER_PORT environment variable to change defult web server port<br>
*cd source*<br>
*python3 app_hello_api.py*
3. Validate endpoints:
  - http://localhost:8080/ - Contains link to documentation
  - http://localhost:8080/api/hello
  - http://localhost:8080/api/health
  - http://localhost:8080/api/ui (Swagger allows to validate enpoints from UI)
4. Open http://localhost:8080/api/ui and execute API calls from UI

### Automation
Docker is used as CRI for containers and minikube for kubernetes validation.<br>
All automation is located in **deploy** folder.

#### Building
All build/deploy vars are defined in scripts/hello.env file<br>
Commands below start building of docker image and push it minikube:<br>
*cd scripts*<br>
*./build.sh*

if you wish to test API service thru docker, then run ./run_docker.sh script

### Kubernetes deployment
Kubernetes deployment is organized thru Helm chart, which located in **deploy/helm** folder
Helm chart has .Values.app.serviceOwner param which defines greeting message in the container<br>

Simple way to install chart with different customer name is:<br>
helm install <release name> <path to helm chart> --set app.serviceOwner=some_name<br>
Example:
*cd deploy/helm*
*helm install hello-api ./hello-api --set app.serviceOwner=customerA*<br>

For execution of kubernetes deployment please run scripts/deploy.sh<br>
The script starts minikube and deploys two charts for CustomerA and CustomerB into **default** namespace.

When deployment is completed, validate that pods are up and running(wait around 30 sec):<br>
*kubectl config set-context minikube*<br>
*kubectl get pods -n default*

API is available on NodePort services, to get access to NodePort endpoints follow these steps:
1. Identify NodePort services<br>
*kubectl get svc -n default*
2. Expose service for customer-a and validate endpoints<br>
*minikube service hello-a-hello-api-customera --url*
3. Expose service for customer-b and validate endpoints<br>
*minikube service hello-b-hello-api-customerb --url*

## Notes
 - Unfortunately, I couldn't fix DNS problems with minikube on my laptop(sudo permissions are restricted), so I didn't use Ingress for exposing services. This is the reason why I decided to use NodePort
 - Containers becomes ready in ~30sec, it's a lot for small service. Need to validate and tune probes setup to improve it. And also check minikube setup
 
## The next steps
it's a bit difficult to develop CI/CD without real hosting and environment requirements, but in general I would create the following pipelines:
1. Merge requests:<br>
Linters(python, dockerfile, helm)<br>
SAST<br>
Scan for sensitive data(like password leaks)<br>
Run application build(if exist) and unit test jobs<br>
2. CI:<br>
Run Semver<br>
Run build(if exist)<br>
Unit tests<br>
Functional tests<br>
Push helm chart to repository(if any changes are exist)<br>
Build docker image upload image to registry<br>
Scan docker image for vulnerabilities<br>
3. CD:<br>
Update repository related with ARGOCD or deploy helm chart<br>
Perfrom basic checks of service<br>
Rollback if something wrong(Depends on deployment strategy, blue-green/canary don't require this step in this place)<br>
Run API tests to make sure that service running properly<br>
Run integration/smoke/etc tests if they are provided by developers/qa team<br>
