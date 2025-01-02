import unittest
from unittest.mock import Mock, patch
from requests.models import Response
from models.imdb import IMDb

# Dados de teste simulados
IMDB_DATA = {
    "GOOD_SEARCH": {
        "searchType": "Title",
        "expression": "Bambi",
        "results": [{"id": "tt1375666", "resultType": "Movie", "image": None, "title": "Bambi", "description": "Disney movie about a baby deer"}],
        "errorMessage": None
    },
    "INVALID_API": {
        "searchType": "Title",
        "expression": "Bambi",
        "results": None,
        "errorMessage": "Invalid API Key"
    },
    "MOVIE_INVALID": {
        "imDbId": None,
        "title": None,
        "fullTitle": None,
        "type": None,
        "year": None,
        "items": None,
        "errorMessage": "Invalid request."
    },
    "GOOD_REVIEW": {
        "imDbId": "tt1375666",
        "title": "Bambi",
        "fullTitle": "Bambi",
        "type": "Movie",
        "year": "1942",
        "items": [{"username": "mickey", "userUrl": None, "reviewLink": None, "warningSpoilers": True, "date": "2008-04-01", "rate": "5", "helpful": None, "title": "Tear jerker", "content": "This movie will make you cry"}],
        "errorMessage": None
    },
    "GOOD_RATING": {
        "imDbId": "tt1375666",
        "title": "Bambi",
        "fullTitle": "Bambi",
        "type": "Movie",
        "year": "1942",
        "imDb": 5,
        "metacritic": 4,
        "theMovieDb": 4,
        "rottenTomatoes": 5,
        "filmAffinity": 3,
        "errorMessage": None
    }
}

class TestIMDb(unittest.TestCase):
    @patch('models.imdb.IMDb.search_titles')
    def test_search_by_title(self, imdb_mock):
        """Test searching by title"""
        imdb_mock.return_value = IMDB_DATA["GOOD_SEARCH"]
        imdb = IMDb("k_12345678")
        results = imdb.search_titles("Bambi")
        self.assertIsNotNone(results)
        self.assertIsNone(results["errorMessage"])
        self.assertIsNotNone(results["results"])
        self.assertEqual(results["results"][0]["id"], "tt1375666")
        self.assertEqual(results["results"][0]["title"], "Bambi")
        self.assertEqual(results["results"][0]["description"], "Disney movie about a baby deer")

    @patch('models.imdb.requests.get')
    def test_search_with_no_results(self, imdb_mock):
        """Test searching with no results"""
        imdb_mock.return_value = Mock(status_code=404)
        imdb = IMDb("k_12345678")
        results = imdb.search_titles("NonExistentTitle")
        self.assertEqual(results, {})

    @patch('models.imdb.requests.get')
    def test_search_by_title_failed(self, imdb_mock):
        """Test searching by title failed"""
        imdb_mock.return_value = Mock(
            spec=Response,
            status_code=200,
            json=Mock(return_value=IMDB_DATA["INVALID_API"])
        )
        imdb = IMDb("bad-key")
        results = imdb.search_titles("Bambi")
        self.assertIsNotNone(results)
        self.assertEqual(results["errorMessage"], "Invalid API Key")
        self.assertIsNone(results["results"])

    @patch('models.imdb.requests.get')
    def test_movie_ratings(self, imdb_mock):
        """Test movie Ratings"""
        imdb_mock.return_value = Mock(
            spec=Response,
            status_code=200,
            json=Mock(return_value=IMDB_DATA["GOOD_RATING"])
        )
        imdb = IMDb("k_12345678")
        results = imdb.movie_ratings("tt1375666")
        self.assertIsNotNone(results)
        self.assertEqual(results["title"], "Bambi")
        self.assertEqual(results["filmAffinity"], 3)
        self.assertEqual(results["rottenTomatoes"], 5)
        self.assertEqual(results["imDb"], 5)

if __name__ == "__main__":
    unittest.main()
