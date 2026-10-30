"""Run only against a disposable local/staging demo deployment, never production."""

import os

from locust import HttpUser, between, task


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
            if "Logout" not in response.text:
                response.failure("Demo login failed; do not interpret response times as authenticated performance.")
                raise RuntimeError("Demo login failed.")

    @task(2)
    def dashboard(self):
        self.client.get("/")

    @task
    def transactions(self):
        self.client.get("/transactions/?month=2026-10")
