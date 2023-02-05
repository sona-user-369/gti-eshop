from locust import HttpUser, task


class ProjectPerfTest(HttpUser):

    @task
    def get_products(self):
        response = self.client.get("/all_product")
    @task
    def home(self):
        response = self.client.get("")