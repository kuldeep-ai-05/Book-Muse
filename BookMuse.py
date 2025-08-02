import streamlit as st
import requests

#API Base URL
#API_BASE="http://127.0.0.1:8000/api"
API_BASE="http://13.201.227.154/api"

#Utility function to store tokens during session
def saveToken(token):
    st.session_state['access_token']=token

def getToken():
    return st.session_state.get('access_token',None)

def clearToken():
    st.session_state.pop('access_token',None)
    st.session_state.pop('username', None)


#__RegistrationPage__

def register():
    st.header("Register New User")
    username=st.text_input("Username:")
    password=st.text_input("password",type="password")
    if st.button("Register"):
        if not username or not password:
            st.error("Please Provide Username and Password.")
            return
        data={"username":username,"password":password}
        try:
            response=requests.post(f"{API_BASE}/register/",json=data)
            if response.status_code==201:
                tokens=response.json()
                st.success(f"User {username} registered !")
                saveToken(tokens['access'])
                st.info("You are now logged In !")
            else:
                st.error(f"Registration Failed: {response.json()}")
        except Exception as e:
            st.error(f"Error Connecting to API:{e}")

#__LoginPage__

def login():
    st.header("User Login")
    username=st.text_input("Username",key='login_username')
    password=st.text_input("Password",type="password",key="login_password")
    if st.button("Login"):
        if not username or not password:
            st.error("Please Enter Username and Password.")
            return

        data={"username":username,"password":password}
        try:
            response=requests.post(f"{API_BASE}/token/",json=data)
            if response.status_code==200:
                tokens=response.json()
                st.success("Logged in Successfully !")
                saveToken(tokens['access'])
                st.session_state['username'] = username
            else:
                st.error(f"Login Failed: {response.json()}")
        except Exception as e:
            st.error(f"Error Connecting to API:{e}")

#__LogoutPage__

def logout():
    clearToken()
    st.success("Logged Out Successfully")

#__AddBooksPage__

def addBook():
    st.header("Add New Book (Admin Only)")

    token = st.text_input("Paste your Admin Access Token here", type="password")

    title = st.text_input("Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    published_year = st.number_input("Published Year", min_value=0, max_value=2100, step=1)

    if st.button("Add Book"):
        if not token:
            st.error("Admin token required to add book.")
            return
        data = {
            "title": title,
            "author": author,
            "genre": genre,
            "published_year": published_year,
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        response = requests.post("http://127.0.0.1:8000/api/books/", json=data, headers=headers)
        if response.status_code == 201:
            st.success("Book added successfully!")
        else:
            st.error(f"Failed to add book: {response.status_code} - {response.text}")

#__ViewBooksPage__

def viewBooks():
    st.header("Book List")
    try:
        response = requests.get(f"{API_BASE}/books/")
        if response.status_code == 200:
            books = response.json()
            #st.write("Raw API Books Response:", books)  # Debug: shows full response

            # Get the list of books from pagination results
            bookList = books.get("results", [])

            if bookList:
                for book in bookList:  # Iterate over bookList here, not books
                    st.subheader(book.get('title', 'No Title'))
                    st.write(f"Author: {book.get('author', 'Unknown')}")
                    st.write(f"Genre: {book.get('genre', 'N/A')}")
                    st.write(f"Published Year: {book.get('published_year', 'Unknown')}")
                    st.markdown("---")
            else:
                st.info("No Books Found")
        else:
            st.error(f"Failed to Fetch Books: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Error Connecting to API: {e}")


#__AddReviewPage__

def addReview():
    st.header("Add a Review")
    token = getToken()
    if not token:
        st.warning("You must be logged in to add a review")
        return
    
    #simple form for review
    bookId=st.number_input("Book ID",min_value=1,step=1)
    rating=st.slider("Rating (1 to 5)",1,5)
    reviewText=st.text_area("Your Review")

    if st.button("Submit Review"):
        if not bookId or not reviewText:
            st.error("Please Fill all Fields")
            return
        
        headers={
            "Authorization":f"Bearer {token}",
            "Content-Type":"application/json"
        }
        data={
            "book":bookId,
            "rating":rating,
            "text":reviewText
        }
        try:
            response=requests.post(f"{API_BASE}/reviews/",headers=headers,json=data)
            if response.status_code==201:
                st.success("Review Submitted Successfully")
            else:
                st.error(f"Failed to submit review:{response.json()}")
        except Exception as e:
            st.error(f"Error Connecting to API: {e}")

#__ViewReviewsForBooksPage__

def viewReviews():
    st.header("View Reviews")
    bookId = st.number_input("Enter Book Id to fetch reviews", min_value=1, step=1, key="view_book_id")
    
    if st.button("Get Reviews"):
        try:
            response = requests.get(f"{API_BASE}/reviews/?book={bookId}")
            if response.status_code == 200:
                data = response.json()
                
                # Extract the list of reviews from paginated results
                reviewList = data.get("results", [])
                
                if reviewList:
                    for review in reviewList:
                        reviewer_username = review.get('reviewer', {}).get('username', 'Anonymous')
                        rating = review.get('rating', 'N/A')
                        text = review.get('text', '')
                        
                        st.markdown(f"**Reviewer:** {reviewer_username}")
                        st.markdown(f"**Rating:** {rating}")
                        st.markdown(f"**Review:** {text}")
                        st.markdown("---")
                else:
                    st.info("No Reviews Found for this book")
            else:
                st.error(f"Failed to fetch Reviews: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Error Connecting to API: {e}")

def myReviews():
    st.header("My Reviews")
    token = getToken()
    username = st.session_state.get("username")
    if not token or not username:
        st.warning("You must be logged in to view and manage your reviews.")
        return

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE}/reviews/", headers=headers)
    if response.status_code == 200:
        reviews = response.json().get("results", [])
        my_reviews = [r for r in reviews if r['reviewer']['username'] == username]
        for review in my_reviews:
            st.markdown(f"**Rating:** {review['rating']}")
            st.markdown(f"**Review:** {review['text']}")
            if st.button(f"Delete Review {review['id']}"):
                delete_resp = requests.delete(f"{API_BASE}/reviews/{review['id']}/", headers=headers)
                if delete_resp.status_code == 204:
                    st.success("Review deleted.")
                else:
                    st.error(f"Failed to delete review: {delete_resp.status_code}")
            st.markdown("---")
    else:
        st.error("Failed to fetch your reviews.")

#__MainApp__

def main():
    st.title("Django Book Review")
    menu=["Register", "Login", "Logout", "View Books", "Add Review", "View Reviews","My Reviews","Add Books"]
    choice=st.sidebar.selectbox("Menu",menu)
    if choice == "Register":
        register()
    elif choice == "Login":
        login()
    elif choice == "Logout":
        logout()
    elif choice == "Add Books":
        addBook()
    elif choice == "View Books":
        viewBooks()
    elif choice == "Add Review":
        addReview()
    elif choice == "My Reviews":
        myReviews()
    elif choice == "View Reviews":
        viewReviews()
    else:
        st.write("Select an option from the sidebar.")

if __name__ == "__main__":
    main()
