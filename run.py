from limbook_api import create_app, Config

# Create flask app
app = create_app(Config)

if __name__ == '__main__':
    app.run(debug=True)
