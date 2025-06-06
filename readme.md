# Spotcheck AI - Skin Lesion Analysis Tool

A Streamlit-based web application that helps users analyze skin lesions for potential malignancy using AI. The application provides two ways to submit images for analysis: through a camera input or by uploading an image file.

## Features

- **Camera Input**: Take a photo directly through your device's camera
- **Image Upload**: Upload existing images (supports JPG, JPEG, and PNG formats)
- **AI Analysis**: Get instant analysis of skin lesions
- **User-friendly Interface**: Simple and intuitive navigation

## Setup

1. Ensure you have Python 3.12.9 installed (as specified in `.python-version`)
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with the following content:
   ```
   API_ENDPOINT=your_api_endpoint_here
   ```
   Note: Contact the project maintainer for the actual API endpoint URL.

## Running the Application

1. Start the Streamlit server:
   ```bash
   streamlit run landing_page.py
   ```
2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## Usage

1. **Landing Page**: Start here to get an overview of the application
2. **Camera Input**:
   - Enable the camera
   - Take a photo of the skin area
   - Click "Scan for malignant spots" to analyze
3. **Image Upload**:
   - Click "Choose an image file" to select an image
   - Preview the uploaded image
   - Click "Scan for malignant spots" to analyze

## Project Structure

```
spot-check-simple-frontend/
├── landing_page.py      # Main landing page
├── pages/
│   ├── 1_Camera_Input.py    # Camera input functionality
│   └── 1_Image_Upload.py    # Image upload functionality
├── requirements.txt     # Python dependencies
├── .env                # Environment variables (not in git)
├── .env.example        # Example environment variables
└── README.md           # This file
```

## API Integration

The application integrates with a machine learning API endpoint for skin lesion analysis. The endpoint URL is configured through environment variable API_ENDPOINT and can be adjusted to your model endpoint.

## Development

To modify or extend the application:
1. The main landing page is in `landing_page.py`
2. Additional pages are in the `pages/` directory
3. Each page is a standalone Streamlit application
4. The order of pages in the navigation is determined by the numeric prefix in the filename
5. Environment variables are loaded from `.env` file using python-dotenv

## Security Notes

- Never commit the `.env` file to version control
- Keep your API endpoint URL private
- Use `.env.example` as a template for required environment variables

## License

[Add your license information here]
