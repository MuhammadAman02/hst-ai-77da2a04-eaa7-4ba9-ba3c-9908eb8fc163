"""
Seiko Watch Store - Main Application
Professional e-commerce platform for luxury Seiko timepieces
"""

from nicegui import ui, app
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.core.config import settings
from app.core.database import get_db_session
from app.core.assets import SeikoAssetManager
from app.core.logger import app_logger
from app.services.product_service import ProductService
from app.services.cart_service import CartService
from app.services.auth_service import AuthService
from app.services.order_service import OrderService
from app.frontend.pages.home import HomePage
from app.frontend.pages.products import ProductsPage
from app.frontend.pages.product_detail import ProductDetailPage
from app.frontend.pages.cart import CartPage
from app.frontend.pages.checkout import CheckoutPage
from app.frontend.pages.auth import AuthPage
from app.frontend.pages.admin import AdminPage
from app.frontend.components.layout import create_layout
from app.api.router import api_router

# Global services
product_service = ProductService()
cart_service = CartService()
auth_service = AuthService()
order_service = OrderService()
asset_manager = SeikoAssetManager()

# Global state
class AppState:
    def __init__(self):
        self.current_user = None
        self.cart_items = []
        self.cart_total = 0.0
        self.selected_product = None
        
app_state = AppState()

def setup_fastapi_app():
    """Configure FastAPI application with middleware and routes"""
    fastapi_app = FastAPI(
        title="Seiko Watch Store API",
        description="Professional e-commerce API for Seiko timepieces",
        version="1.0.0"
    )
    
    # Add CORS middleware
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Mount static files
    fastapi_app.mount("/static", StaticFiles(directory="app/static"), name="static")
    
    # Include API routes
    fastapi_app.include_router(api_router, prefix="/api")
    
    return fastapi_app

@ui.page('/')
async def home():
    """Seiko Watch Store Homepage"""
    with create_layout("Seiko Watch Store - Premium Timepieces", app_state):
        home_page = HomePage(product_service, asset_manager, app_state)
        await home_page.render()

@ui.page('/products')
async def products():
    """Products catalog page"""
    with create_layout("Shop Seiko Watches", app_state):
        products_page = ProductsPage(product_service, asset_manager, app_state)
        await products_page.render()

@ui.page('/product/{product_id}')
async def product_detail(product_id: int):
    """Individual product detail page"""
    with create_layout("Seiko Watch Details", app_state):
        detail_page = ProductDetailPage(product_service, cart_service, asset_manager, app_state)
        await detail_page.render(product_id)

@ui.page('/cart')
async def cart():
    """Shopping cart page"""
    with create_layout("Shopping Cart", app_state):
        cart_page = CartPage(cart_service, asset_manager, app_state)
        await cart_page.render()

@ui.page('/checkout')
async def checkout():
    """Checkout process page"""
    with create_layout("Checkout", app_state):
        checkout_page = CheckoutPage(order_service, asset_manager, app_state)
        await checkout_page.render()

@ui.page('/auth')
async def auth():
    """Authentication page (login/register)"""
    with create_layout("Account", app_state):
        auth_page = AuthPage(auth_service, app_state)
        await auth_page.render()

@ui.page('/admin')
async def admin():
    """Admin panel for store management"""
    with create_layout("Admin Panel", app_state):
        admin_page = AdminPage(product_service, order_service, app_state)
        await admin_page.render()

def create_seiko_store():
    """Create and run the Seiko Watch Store"""
    try:
        # Setup FastAPI app
        fastapi_app = setup_fastapi_app()
        
        # Configure NiceGUI
        ui.run(
            host=settings.host,
            port=settings.port,
            title="Seiko Watch Store",
            favicon="🕰️",
            dark=False,
            language='en',
            reload=settings.debug,
            show=settings.debug,
            app=fastapi_app,
            storage_secret=settings.secret_key
        )
        
    except Exception as e:
        app_logger.error(f"Failed to start Seiko Watch Store: {e}")
        raise

if __name__ in {"__main__", "__mp_main__"}:
    create_seiko_store()