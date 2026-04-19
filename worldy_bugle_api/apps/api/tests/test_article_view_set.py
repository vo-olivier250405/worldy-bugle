from pytest import mark


@mark.django_db
class TestArticleViewSet:
    url = "/api/articles/"

    def test_should_returns_list(self, client):
        response = client.get(self.url)
        assert response.status_code == 200

    def test_should_returns_404_on_unknown(self, client):
        response = client.get(f"{self.url}fake-uuid/")
        assert response.status_code == 404

    def test_should_returns_retrieve(self, client, article):
        response = client.get(f"{self.url}{article.id}/")
        assert response.status_code == 200
        assert response.data["id"] == str(article.id)

    def test_should_returns_paginated_list(self, client, paginated_response_attributes):
        response = client.get(self.url)
        assert response.status_code == 200
        for attribute in paginated_response_attributes:
            assert attribute in response.data

    def test_should_not_create_article(self, client):
        response = client.post(self.url, body={})
        assert response.status_code == 405

    def test_should_not_delete_article(self, client, article):
        response = client.delete(self.url + str(article.id) + "/")
        assert response.status_code == 405

    def test_should_not_update_article(self, client, article):
        response = client.patch(f"{self.url}{str(article.id)}/", body={})
        assert response.status_code == 405
