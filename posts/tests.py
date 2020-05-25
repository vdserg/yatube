from django.test import TestCase, Client

from posts.models import User, Post


class PostTest(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            username="testuser", email="test@test.com",
            password="12345"
        )

    def test_profile(self):
        response = self.client.get("/testuser/")

        self.assertEqual(response.status_code, 200)

    def test_user_can_post(self):
        user = User.objects.get(username="testuser")
        self.client.force_login(user)
        response = self.client.get("/new/")
        self.assertEqual(
            response.status_code, 200,
        )

    def test_nonuser_cant_post(self):
        response = self.client.get("/new/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/auth/login/?next=/new/")

    def test_created_post_on_pages(self):
        user = User.objects.get(username="testuser")
        self.client.force_login(user)
        self.client.post("/new/", {"text": "Test post", "author": user})
        post = Post.objects.get(text="Test post")
        response = self.client.get("")
        self.assertEqual(response.context["post"], post)

        response = self.client.get(f"/{user}/{post.id}/")
        self.assertEqual(response.context["post"], post)

        response = self.client.get(f"/{user}/")
        self.assertEqual(response.context["post"], post)

    def test_user_can_edit_his_post(self):
        user = User.objects.get(username="testuser")
        self.client.force_login(user)
        post = Post.objects.create(text="Test post", author=user)
        self.client.post(f"/{user.username}/{post.id}/edit/",
                         {"text": "Post edit", "author": user,
                          "post_id": post.id})
        response = self.client.get("")
        self.assertNotEqual(response.context["post"].text, post.text)

        response = self.client.get(f"/{user}/{post.id}/")
        self.assertNotEqual(response.context["post"].text, post.text)

        response = self.client.get(f"/{user}/")
        self.assertNotEqual(response.context["post"].text, post.text)
