from django.urls import path
from finances.api.views.categorie_views import (
    CategorieListCreateView,
    CategorieDetailView
)
from finances.api.views.compte_views import (
    CompteListCreateView,
    CompteDetailView,
    CompteSoldeView
)
from finances.api.views.transaction_views import (
    TransactionListCreateView,
    TransactionDetailView,
    TransactionStatistiquesView
)
from finances.api.views.transfert_views import (
    TransfertListCreateView,
    TransfertDetailView
)
from finances.api.views.budget_views import (
    BudgetListCreateView,
    BudgetDetailView,
    BudgetEtatView
)

urlpatterns = [

    # ─────────────────────────────────────
    # CATEGORIES
    # ─────────────────────────────────────
    path(
        'categories/',
        CategorieListCreateView.as_view(),
        name='categorie-list-create'
    ),
    path(
        'categories/<int:pk>/',
        CategorieDetailView.as_view(),
        name='categorie-detail'
    ),

    # ─────────────────────────────────────
    # COMPTES
    # ─────────────────────────────────────
    path(
        'comptes/',
        CompteListCreateView.as_view(),
        name='compte-list-create'
    ),
    path(
        'comptes/<int:pk>/',
        CompteDetailView.as_view(),
        name='compte-detail'
    ),
    path(
        'comptes/solde/',
        CompteSoldeView.as_view(),
        name='compte-solde'
    ),

    # ─────────────────────────────────────
    # TRANSACTIONS
    # ─────────────────────────────────────
    path(
        'transactions/',
        TransactionListCreateView.as_view(),
        name='transaction-list-create'
    ),
    path(
        'transactions/<int:pk>/',
        TransactionDetailView.as_view(),
        name='transaction-detail'
    ),
    path(
        'transactions/statistiques/',
        TransactionStatistiquesView.as_view(),
        name='transaction-statistiques'
    ),

    # ─────────────────────────────────────
    # TRANSFERTS
    # ─────────────────────────────────────
    path(
        'transferts/',
        TransfertListCreateView.as_view(),
        name='transfert-list-create'
    ),
    path(
        'transferts/<int:pk>/',
        TransfertDetailView.as_view(),
        name='transfert-detail'
    ),

    # ─────────────────────────────────────
    # BUDGETS
    # ─────────────────────────────────────
    path(
        'budgets/',
        BudgetListCreateView.as_view(),
        name='budget-list-create'
    ),
    path(
        'budgets/<int:pk>/',
        BudgetDetailView.as_view(),
        name='budget-detail'
    ),
    path(
        'budgets/etat/',
        BudgetEtatView.as_view(),
        name='budget-etat'
    ),
]