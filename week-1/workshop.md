Follow the instructions to do the hands-on pairing for Week 1.

-----

## 🤝 Hands-On Pairing: The API Client & Postman

The goal of this exercise is for you and your pairing peer to act as API detectives. You'll use two resources—a simple pre-built web page and a Postman Collection—to reverse-engineer what the front-end application is trying to do. This will help you understand the client's perspective and the importance of a well-defined API "contract."

### **Part 1: The Front-End Code Detective Work**

**Objective:** To identify API-related actions and requirements by reading and understanding a simple HTML and JavaScript codebase.

#### **Pairing Instructions**

1.  **Analyze `script.js`**: Look at the two main sections of the code, one for fetching posts and one for creating a new post.
2.  **Identify Endpoints and Methods**: What's the base URL? What HTTP method is used for fetching? What method is used for creating?
3.  **Identify Request and Response Formats**:
      * For the **`GET`** request, what does the code expect to receive from the server (e.g., is it an array, and what keys does it use)?
      * For the **`POST`** request, what data is the client sending in the request body?

### **Part 2: The Postman Sandbox**

**Objective:** Use Postman to manually replicate the requests from the front-end code and observe the server's responses.

**Task:**

1.  **Open Postman** and create a new request.
2.  **Recreate the `GET` Request:**
      * Set the HTTP method to **`GET`**.
      * Paste the API URL: `https://jsonplaceholder.typicode.com/posts`.
      * Send the request and examine the response body. Does it match what the front-end code expects?
3.  **Recreate the `POST` Request:**
      * Set the HTTP method to **`POST`**.
      * Paste the same API URL.
      * Go to the **Body** tab, select **`raw`**, and choose **`JSON`** from the dropdown.
      * Paste the JSON object from the `script.js` file into the body.
        ```json
        {
            "title": "foo",
            "body": "bar",
            "userId": 1
        }
        ```
      * Send the request and observe the server's response. What is the status code? What new data did the server return?

### **Weekly Project & Homework**

  * **Document Your Findings:** Create a short document summarizing your discoveries from the code analysis and Postman testing.
  * **Homework:** Using Postman, deliberately send a **`POST`** request with a missing **`title`** or **`body`** field. What status code do you receive? What error message (if any) does the server provide? This teaches you how to troubleshoot common API errors.