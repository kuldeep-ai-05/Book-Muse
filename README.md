# Book Review Frontend (Streamlit App)

This repository contains the Streamlit frontend application that consumes the Book Review API backend. It provides a user-friendly interface for users to register, login, view books, add reviews, and manage their profiles.

![Book-Muse](https://github.com/user-attachments/assets/9f6e1f41-c66b-4a25-9633-9245bbbb4738)

---

## Features

- User registration and login form with JWT authentication
- View list of books and detailed reviews
- Add new reviews (authenticated users)
- Admin functionality to add books (requires token)
- Session handling with Streamlit state

---

## Tech Stack

- Python 3.10+
- Streamlit
- Requests library for API calls
- Docker for containerization

---

## Getting Started

### Prerequisites

- Python 3.10+
- Docker (optional, for container deployment)
- Running instance of Book Review API backend accessible via public IP or domain

### Local Setup

1. Clone this repository:

    ```
    git clone https://github.com/yourusername/book-review-frontend.git
    cd book-review-frontend
    ```

2. Create and activate a virtual environment:

    ```
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

4. Update the API base URL in the code (`app.py` or wherever `API_BASE` is defined):

    ```
    API_BASE = "http://<ec2_public_ip_or_domain>/api"
    ```

5. Run the Streamlit app locally:

    ```
    streamlit run app.py
    ```

---

## Docker Deployment

### Build Docker Image

```
docker build -t book-review-frontend .
```


### Tag and Push to AWS ECR (replace placeholders)

```
docker tag book-review-frontend:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/book-review-frontend:latest
docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/book-review-frontend:latest
```


### Run on EC2

```
sudo docker run -d -p 8501:8501 <aws_account_id>.dkr.ecr.<region>.amazonaws.com/book-review-frontend:latest
```


---

## Notes

- Ensure `API_BASE` points to the live backend API URL.
- For easier deployment, consider using environment variables to configure API base URL dynamically.
- The app requires backend API to be accessible from the frontend container/network.

---

## License

MIT License

---

## Contact

For questions or contributions, contact [kuldeep.mca2024@example.com]


