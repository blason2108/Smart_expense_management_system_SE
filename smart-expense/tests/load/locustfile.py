"""Run only against a disposable local/staging demo deployment, never production."""

import os

from locust import HttpUser, between, task
from locust.exception import StopUser


class FinanceUser(HttpUser):
    wait_time = between(0.5, 1.5)

    def on_start(self):
        password = os.environ.get("DEMO_PASSWORD")
        if not password:
            raise RuntimeError("Set DEMO_PASSWORD for the seeded demo user.")
        self.client.get("/accounts/login/")
        token = self.client.cookies.get("csrftoken")
        with self.client.post(
            "/accounts/login/",
            data={"username": "demo", "password": password, "csrfmiddlewaretoken": token},
            headers={"Referer": self.host + "/accounts/login/"},
            catch_response=True,
        ) as response:
            logged_in = response.status_code == 200 and "Logout" in response.text
            if not logged_in:
                response.failure("Demo login failed; do not interpret response times as authenticated performance.")
        if not logged_in:
            raise StopUser()

    def authenticated_get(self, path, name):
        with self.client.get(path, name=name, allow_redirects=False, catch_response=True) as response:
            if response.status_code != 200 or "Logout" not in response.text:
                response.failure("Expected an authenticated page.")

    @task(2)
    def dashboard(self):
        self.authenticated_get("/", "/")

    @task
    def transactions(self):
        self.authenticated_get("/transactions/?month=2026-10", "/transactions/ (October)")
