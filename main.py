from app.service import service

app = service.get_app()

if __name__ == "__main__":
    service.serve(path_to_app="main:app")
