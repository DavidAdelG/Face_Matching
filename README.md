# 🌟 E-Tourism Face Recognition API

This is a FastAPI-based project for E-Tourism, developed as a part of a graduation project. The API provides functionalities for adding, searching, and verifying persons using face recognition technology.

## Features ✨

- **Add Person**: Add a person to the database using an image or a base64-encoded image.
- **Search Person**: Search for a person using an image or a base64-encoded image.
- **Face Matching**: Verify if an image matches a specific person using ID.
- **Historical Search**: Search within a historical collection of characters.
- **Reserve Person**: Make a reservation.
- **Delete Person**: Remove a person from the database.

## Endpoints 🚀

### List All Persons 📋
- **Endpoint**: `/list`
- **Method**: `GET`
- **Description**: Retrieve a list of all persons in the database.

### Add Person ➕
- **Endpoint**: `/add-person`
- **Method**: `POST`
- **Parameters**:
  - `person_name`: The name of the person.
  - `image_file`: The image file of the person.
- **Description**: Add a new person using an uploaded image.

### Add Person (Base64) ➕
- **Endpoint**: `/add-personBase64`
- **Method**: `POST`
- **Parameters**:
  - `person_name`: The name of the person.
  - `image_base64`: The base64-encoded image of the person.
- **Description**: Add a new person using a base64-encoded image.

### Face Matching 🔍
- **Endpoint**: `/face-matching`
- **Method**: `POST`
- **Parameters**:
  - `person_id`: The ID of the person.
  - `image_file`: The image file for matching.
- **Description**: Verify if the uploaded image matches the given person ID.

### Face Matching (Base64) 🔍
- **Endpoint**: `/face-matchingBase64`
- **Method**: `POST`
- **Parameters**:
  - `person_id`: The ID of the person.
  - `image_base64`: The base64-encoded image for matching.
- **Description**: Verify if the base64-encoded image matches the given person ID.

### Search by Image 🔎
- **Endpoint**: `/search-by-image`
- **Method**: `POST`
- **Parameters**:
  - `image_file`: The image file to search.
- **Description**: Search for a person using an uploaded image.

### Search by Image (Base64) 🔎
- **Endpoint**: `/search-by-imageBase64`
- **Method**: `POST`
- **Parameters**:
  - `image_base64`: The base64-encoded image to search.
- **Description**: Search for a person using a base64-encoded image.

### Search by Image in Historical Collection 🏛️
- **Endpoint**: `/historical-by-image`
- **Method**: `POST`
- **Parameters**:
  - `image_file`: The image file to search within the historical collection of characters.
- **Description**: Search for a person in the historical collection using an uploaded image.

### Search by Image in Historical Collection (Base64) 🏛️
- **Endpoint**: `/historical-by-image-base64`
- **Method**: `POST`
- **Parameters**:
  - `image_base64`: The base64-encoded image to search within the historical collection of characters.
- **Description**: Search for a person in the historical collection using a base64-encoded image.

### Search by ID 🆔
- **Endpoint**: `/search-by-id`
- **Method**: `POST`
- **Parameters**:
  - `person_id`: The ID of the person.
- **Description**: Search for a person by their ID.

### Reserve Person 🔒
- **Endpoint**: `/reserve-person`
- **Method**: `POST`
- **Parameters**:
  - `person_id`: The ID of the person to make reservation for.
- **Description**: Make Reservation.

### Delete Person 🗑️
- **Endpoint**: `/delete-person`
- **Method**: `DELETE`
- **Parameters**:
  - `person_id`: The ID of the person to delete.
- **Description**: Remove a person from the database.

## Setup and Deployment ⚙️

### Prerequisites

- Python 3.8+
- FastAPI
- Uvicorn
- PIL
- Other dependencies listed in `requirements.txt`

### Running the Application 🏃‍♂️

1. **Clone the repository**:
    ```bash
    git clone https://github.com/DavidAdelG/Face_Matching
    cd Face_Matching
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set environment variables**:
    ```bash
    export BACKEND_URL=<backend-url>
    export DEVELOPER_KEY=<developer-key>
    ```

4. **Run the application**:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

### Deployment on Render 🌐

1. **Connect your repository** to Render.
2. **Set the environment variables** in the Render dashboard.
3. **Deploy the application** with the start command:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
