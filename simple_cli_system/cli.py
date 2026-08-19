# This CLI script sends HTTP requests to our FastAPI server

import typer
import requests

app = typer.Typer(help="CLI tool to manage PostgreSQL users via FastAPI.")
API_URL = "http://127.0.0.1:8000"

@app.command()
def create(username: str, email: str):
    """ Add a new user to the database """
    payload = {"username": username, "email": email}
    response = requests.post(f"{API_URL}/users/", json=payload)

    if response.status_code == 200:
        data = response.json()
        typer.echo(f"User Created Successfully! ID: {data['user_id']}")
    else:
        typer.echo(f"Error: {response.text}")


@app.command()
def list_users():
    """ List all users from the database """
    response = requests.get(f"{API_URL}/users/")

    if response.status_code ==200:
        users = response.json()
        if not users:
            typer.echo("No users found.")
            return

        typer.echo("\n--- Registered Users ---")
        for u in users:
            typer.echo(f"ID: {u['user_id']} | Username: {u['username']} | Email: {u['email']}")
    else:
        typer.echo(f"Failed to fetch Users: {response.text}")

if __name__ == "__main__":
    app()