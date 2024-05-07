# ai-aplication

# NLP Projects

This project is designed as an application to classify natural language processing (NLP) models. Specifically, it includes NLP techniques such as Named Entity Recognition (NER).

## About the Project

Named Entity Recognition (NER) is a significant technique in the field of Natural Language Processing (NLP). This technique is used to identify specific entity types (such as names, locations, dates, organizations, etc.) within texts. NER models utilize learning algorithms to identify and classify specific entity types within texts. This technique is widely used in many applications that involve understanding and processing text data.

This application provides a tool for classifying NER and similar NLP models, allowing for more effective processing and understanding of text data.

## How to Use

1. **Clone the Project**: Clone this repository to your server to start the application.
2. **Build the Images**: Run ./docker-build.sh to build the images.
3. **Run Docker Compose**: Execute the command docker-compose up.
4. **Access the Web Application**: Navigate to `http://localhost:80` in your browser to access the application.
5. **Enter Text**: Enter the text you want to analyze into the input field on the application's interface.
6. **Make Predictions**: Click the "Predict" button to process the text and view the results.

## For Developers

- This application is developed using Flask.
- The Hugging Face Transformers library is used for natural language processing (NLP).
- MySQL is used for the database.

## License

This project is licensed under the MIT License. For more information, see the [LICENSE](LICENSE) file.
