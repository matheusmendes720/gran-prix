from locust import HttpUser, task, between


class BacenUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_exchange_rate(self):
        with self.client.get(
            "/dados/serie/bcdata.sgs.1/dados",
            params={"formato": "json", "dataInicial": "01/01/2024", "dataFinal": "31/12/2024"},
            timeout=5.0,
            catch_response=True,
        ) as response:
            if response.status_code not in (200, 204):
                response.failure(f"Unexpected status {response.status_code}")
