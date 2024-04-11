from rest_framework.routers import SimpleRouter

from vticket_app.views.profile_view import ProfileView

router = SimpleRouter(False)
router.register("profile", ProfileView, "profile")
urls = router.urls