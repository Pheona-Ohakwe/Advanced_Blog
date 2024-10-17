
import unittest
from unittest.mock import MagicMock, patch
from app import app
from faker import Faker

fake = Faker()

class TestTokenEndpoint(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('app.routes.encode_token')
    @patch('app.routes.db.session.scalars')
    @patch('app.routes.check_password_hash')
    
    def test_successful_authenticate(self, mock_check_hash, mock_scalars, mock_encode_token):
        mock_user = MagicMock()
        mock_user.id = 123
        
        mock_query = MagicMock()
        mock_query.first.return_value = mock_user
        
        mock_scalars.return_value = mock_query

        mock_check_hash.return_value = True
        
        mock_encode_token.return_value = 'random.jwt.token'

        request_body = {
            "username": fake.user_name(),
            "password": fake.password()
        }

        response = self.client.post('/token', json=request_body)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['token'], 'random.jwt.token')


    def test_unauthorized_user(self):
        request_body = {
            "username": fake.user_name(),
            "password": fake.password()
        }

        response = self.client.post('/token', json=request_body)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['error'], 'Username and/or password is incorrect')
        

# User Endpoints
    @patch('app.routes.db.session.execute')
    @patch('app.routes.token_auth.login_required')
    def test_get_all_users(self, mock_login_required, mock_execute):
        mock_users = [MagicMock() for _ in range(3)]
        mock_execute.return_value.scalars().all.return_value = mock_users
        
        response = self.client.get('/users')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)

    @patch('app.routes.db.session.get')
    @patch('app.routes.token_auth.login_required')
    def test_get_single_user(self, mock_login_required, mock_get):
        mock_user = MagicMock()
        mock_user.id = 1
        mock_get.return_value = mock_user

        response = self.client.get('/users/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], 1)

    def test_create_user(self):
        request_body = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "username": fake.user_name(),
            "email": fake.email(),
            "password": fake.password()
        }

        with patch('app.routes.db.session.add') as mock_add, patch('app.routes.db.session.commit') as mock_commit:
            response = self.client.post('/users', json=request_body)

            self.assertEqual(response.status_code, 201)
            self.assertIn('id', response.json)

    @patch('app.routes.User.query.get')
    @patch('app.routes.token_auth.login_required')
    def test_update_user(self, mock_login_required, mock_get):
        mock_user = MagicMock()
        mock_get.return_value = mock_user

        request_body = {
            "first_name": fake.first_name()
        }

        with patch('app.routes.db.session.commit') as mock_commit:
            response = self.client.put('/users/1', json=request_body)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'User updated successfully')

    @patch('app.routes.User.query.get')
    @patch('app.routes.token_auth.login_required')
    def test_delete_user(self, mock_login_required, mock_get):
        mock_user = MagicMock()
        mock_get.return_value = mock_user

        with patch('app.routes.db.session.delete') as mock_delete, patch('app.routes.db.session.commit') as mock_commit:
            response = self.client.delete('/users/1')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'User deleted successfully')

    # Post Endpoints
    @patch('app.routes.db.session.query')
    @patch('app.routes.token_auth.login_required')
    def test_get_all_posts(self, mock_login_required, mock_query):
        mock_posts = [MagicMock() for _ in range(3)]
        mock_query.return_value.all.return_value = mock_posts

        response = self.client.get('/posts')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)

    @patch('app.routes.db.session.query')
    @patch('app.routes.token_auth.login_required')
    def test_get_single_post(self, mock_login_required, mock_query):
        mock_post = MagicMock()
        mock_post.id = 1
        mock_query.return_value.get.return_value = mock_post

        response = self.client.get('/posts/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], 1)

    def test_create_post(self):
        request_body = {
            "title": fake.sentence(),
            "body": fake.text(),
            "user_id": 1
        }

        with patch('app.routes.db.session.add') as mock_add, patch('app.routes.db.session.commit') as mock_commit:
            response = self.client.post('/posts', json=request_body)

            self.assertEqual(response.status_code, 201)
            self.assertIn('id', response.json)

    @patch('app.routes.Post.query.get')
    @patch('app.routes.token_auth.login_required')
    def test_update_post(self, mock_login_required, mock_get):
        mock_post = MagicMock()
        mock_get.return_value = mock_post

        request_body = {
            "title": fake.sentence()
        }

        with patch('app.routes.db.session.commit') as mock_commit:
            response = self.client.put('/posts/1', json=request_body)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'Post updated successfully')

    @patch('app.routes.Post.query.get')
    @patch('app.routes.token_auth.login_required')
    def test_delete_post(self, mock_login_required, mock_get):
        mock_post = MagicMock()
        mock_get.return_value = mock_post

        with patch('app.routes.db.session.delete') as mock_delete, patch('app.routes.db.session.commit') as mock_commit:
            response = self.client.delete('/posts/1')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'Post deleted successfully')

    # Comment Endpoints
    @patch('app.routes.db.session.query')
    @patch('app.routes.token_auth.login_required')
    def test_get_all_comments(self, mock_login_required, mock_query):
        mock_comments = [MagicMock() for _ in range(3)]
        mock_query.return_value.all.return_value = mock_comments

        response = self.client.get('/comments')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)

    @patch('app.routes.db.session.query')
    @patch('app.routes.token_auth.login_required')
    def test_get_single_comment(self, mock_login_required, mock_query):
        mock_comment = MagicMock()
        mock_comment.id = 1
        mock_query.return_value.get.return_value = mock_comment

        response = self.client.get('/comments/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], 1)

    def test_create_comment(self):
        request_body = {
            "content": fake.sentence(),
            "user_id": 1,
            "post_id": 1
        }

        with patch('app.routes.db.session.add') as mock_add, patch('app.routes.db.session.commit') as mock_commit:
            response = self.client.post('/comments', json=request_body)

            self.assertEqual(response.status_code, 201)
            self.assertIn('id', response.json)

    @patch('app.routes.Comment.query.get')
    @patch('app.routes.token_auth.login_required')
    def test_update_comment(self, mock_login_required, mock_get):
        mock_comment = MagicMock()
        mock_get.return_value = mock_comment

        request_body = {
            "content": fake.sentence()
        }

        with patch('app.routes.db.session.commit') as mock_commit:
            response = self.client.put('/comments/1', json=request_body)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'Comment updated successfully')

    @patch('app.routes.Comment.query.get')
    @patch('app.routes.token_auth.login_required')
    def test_delete_comment(self, mock_login_required, mock_get):
        mock_comment = MagicMock()
        mock_get.return_value = mock_comment

        with patch('app.routes.db.session.delete') as mock_delete, patch('app.routes.db.session.commit') as mock_commit:
            response = self.client.delete('/comments/1')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'Comment deleted successfully')


if __name__ == '__main__':
    unittest.main()        
