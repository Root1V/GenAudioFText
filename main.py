from app.app import Main

if __name__ == "__main__":
    print("App:\n")

    app = Main()
    result = app.generate_text("Escribe una breve historia sobre la AGI")
    print(result)
