from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .proof_views import proof_viewer

router = DefaultRouter()
router.register(r'conteneurs', views.ConteneurViewSet)
router.register(r'participations', views.ParticipationViewSet)
router.register(r'portefeuilles', views.PortefeuilleViewSet, basename='portefeuille')
router.register(r'transactions', views.TransactionViewSet, basename='transaction')
router.register(r'taux-change', views.TauxDeChangeViewSet)
router.register(r'fournisseurs', views.FournisseurViewSet)

urlpatterns = [
    path('auth/demander-otp/', views.demander_otp, name='demander-otp'),
    path('auth/verifier-otp/', views.verifier_otp, name='verifier-otp'),
    path('proof/<int:participation_id>/', proof_viewer, name='proof-viewer'),
    path('', include(router.urls)),
]
