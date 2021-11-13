from website import create_app

app = create_app()

# Only run the website if we run this exact statement that couples this file (main.py) with the create_app function.
# use debug for developing easiere.
if __name__ == '__main__':
    app.run(debug=True)
