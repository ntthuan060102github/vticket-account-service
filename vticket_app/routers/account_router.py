from rest_framework.routers import SimpleRouter

from vticket_app.views.account_view import AccountView

router = SimpleRouter(False)
router.register("account", AccountView, "account")
urls = router.urls