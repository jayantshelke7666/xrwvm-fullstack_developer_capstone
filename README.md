# Cars Dealerships Capstone

A full-stack dealership directory and customer review site, built for the IBM Full-Stack Application Development Capstone. The project includes a Django application, React interface, Express data API, and sentiment-analysis service.

## Features

- Browse dealership branches and filter by state.
- Register, log in, and leave dealership reviews.
- Display review sentiment with each customer review.
- Manage users and car makes/models through Django admin.
- Run locally without Docker; the Express service reads the supplied JSON dataset and persists submitted reviews to `server/database/data/reviews.json`.

## Local setup (Windows PowerShell)

Open three PowerShell windows from the repository root.

1. Install Python dependencies into the project folder:

   ```powershell
   $python = 'C:\Users\shelk\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
   $env:TEMP = Join-Path $PWD 'work\tmp'
   New-Item -ItemType Directory -Force $env:TEMP | Out-Null
   & $python -m pip install --target server\.python_packages -r server\requirements.txt Flask
   ```

2. Start the dealership data API:

   ```powershell
   cd server\database
   npm install
   node app.js
   ```

3. Start the sentiment API in another window:

   ```powershell
   cd server\djangoapp\microservices
   & $python -m flask --app app run --host 127.0.0.1 --port 5050
   ```

4. Start Django in another window and prepare its database first:

   ```powershell
   cd server
   $env:PYTHONPATH = (Join-Path $PWD '.python_packages')
   & $python manage.py migrate
   & $python manage.py makemigrations djangoapp
   & $python manage.py migrate
   & $python manage.py shell -c "from djangoapp.populate import initiate; initiate()"
   & $python manage.py runserver
   ```

   Admin login: `root` / `RootPass123!` (change this before deploying).

5. In another window, run the React development site:

   ```powershell
   cd server\frontend
   npm install
   npm start
   ```

   Open `http://localhost:3000`. Django APIs are proxied to `http://127.0.0.1:8000`.

## Main API routes

- `POST /djangoapp/register`, `POST /djangoapp/login`, `GET /djangoapp/logout`
- `GET /djangoapp/get_dealers`, `GET /djangoapp/get_dealers/Kansas`
- `GET /djangoapp/dealer/1`, `GET /djangoapp/reviews/dealer/1`
- `POST /djangoapp/add_review`
- `GET /djangoapp/get_carmakes`, `GET /djangoapp/get_cars`

Express API: `http://localhost:3030/fetchDealers`, `/fetchDealers/Kansas`, `/fetchDealer/1`, `/fetchReviews/dealer/1`.
Sentiment API: `http://localhost:5050/analyze/Fantastic%20services`.

## GitHub and cloud submission

Create your own public GitHub repository from this project and push your work. The README file, source files, workflow output, and evidence images can then be linked or uploaded in the assignment. Deployment requires an IBM Cloud account and your own Code Engine project/credentials; do not publish passwords or cloud tokens in this repository.
