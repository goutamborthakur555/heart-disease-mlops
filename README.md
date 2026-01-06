
**Step 1: Environment & Directory Setup**


	1. Create a virtual environment:
	
*python -m venv venv*

*source venv/bin/activate  # On Windows: venv\Scripts\activate*

	2. Install dependencies:
*pip install -r requirements.txt*

	3. Create necessary directories:

*mkdir data*

*mkdir models*

**Step 2: Data Acquisition & EDA (Verify data is downloaded and saved correctly)**
	
	1. Run the loader:

*python src/data_loader.py*

	2. Verification:
	
		* Check if the file exists: ls data/heart.csv*

**Step 3: Training & Experiment Tracking (Train the model, log to MLflow, and save the artifact)**

	1. Run the training script:
python src/train.py
	2. Verification:
		○ Check if the model is saved: ls models/best_model.pkl
		○ Check MLflow: Run mlflow ui in your terminal, then open http://127.0.0.1:5000 in your browser. You should see your experiments logged there.
		○ Take a screenshot of the MLflow dashboard.

**Step 4: Automated Testing**

Goal: Ensure your code passes the unit tests defined in tests/.
	1. Run Pytest:
Bash

pytest tests/
	2. Verification:
		○ You should see green text indicating tests passed (e.g., 2 passed in 0.45s).
		○ Take a screenshot of the passing tests.

**Step 5: Docker Containerization**

Goal: Package the application and run it as a container.
	1. Build the image: (Make sure you are in the root directory where the Dockerfile is)
Bash

docker build -t heart-disease-api:latest .
	2. Run the container:
Bash

docker run -p 8000:8000 heart-disease-api:latest
	3. Test the API (Prediction): Open a new terminal and send a test request:
Bash

curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'Content-Type: application/json' \
  -d '{
  "age": 63, "sex": 1, "cp": 3, "trestbps": 145, "chol": 233, "fbs": 1,
  "restecg": 0, "thalach": 150, "exang": 0, "oldpeak": 2.3, "slope": 0,
  "ca": 0, "thal": 1
}'
		○ Response should be: {"heart_disease_prediction": 1, "confidence": ...}.
		○ Take a screenshot of the docker build command and the curl response.

**Step 6: Kubernetes Deployment**

Goal: Deploy the Docker container to a local Kubernetes cluster.
	1. Start Minikube:
Bash

minikube start
	2. Load Image into Minikube: Since the image is local, you need to load it into Minikube's cache so it can find it without pulling from Docker Hub:
Bash

minikube image load heart-disease-api:latest
	3. Update Deployment File:
		○ Open k8s-deployment file.
		○ Change image: your-docker-username/heart-disease-api:latest to image: heart-disease-api:latest.
		○ Ensure imagePullPolicy: Never is added under the image line (important for local testing).
	4. Deploy:
Bash

kubectl apply -f k8s-deployment
	5. Expose & Verify:
		○ Check status: kubectl get pods (Wait until Status is Running).
		○ Get the URL: minikube service heart-disease-service --url
		○ Use that URL to test the API again using curl or Postman.
		○ Take screenshots of kubectl get pods and the final API test.

**Step 7: CI/CD Pipeline (GitHub Actions)**

Goal: Verify the pipeline runs on GitHub.
	1. Push to GitHub:
		○ Initialize git (git init), add files, commit, and push to a new GitHub repository.
	2. Secrets:
		○ Go to your GitHub Repo -> Settings -> Secrets and variables -> Actions.
		○ Add DOCKER_USERNAME and DOCKER_PASSWORD.
	3. Check Actions:
		○ Go to the "Actions" tab in your repo. You should see the workflow running.
Take a screenshot of the green success checkmarks.<img width="880" height="3026" alt="image" src="https://github.com/user-attachments/assets/819ab01f-260e-4513-b154-545d04f5acb4" />

