from rest_framework.routers import SimpleRouter

from vticket_app.views.user_view import UserView

router = SimpleRouter(False)
router.register("user", UserView, "user")
urls = router.urls