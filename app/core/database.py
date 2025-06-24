"""
Database configuration and models for Seiko Watch Store
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Generator
import os

from app.core.config import settings
from app.core.logger import app_logger

# Database setup
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    orders = relationship("Order", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    image_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    model_number = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    original_price = Column(Float)  # For sale pricing
    stock_quantity = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    # Watch-specific attributes
    movement_type = Column(String(50))  # Automatic, Quartz, Solar, etc.
    case_material = Column(String(50))  # Stainless Steel, Titanium, etc.
    case_diameter = Column(String(20))  # 42mm, etc.
    water_resistance = Column(String(50))  # 100m, 200m, etc.
    strap_material = Column(String(50))  # Leather, Steel, Rubber, etc.
    
    # Images
    main_image_url = Column(String(500))
    detail_image_url = Column(String(500))
    lifestyle_image_url = Column(String(500))
    
    # Status
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    is_on_sale = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")

class CartItem(Base):
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Order details
    total_amount = Column(Float, nullable=False)
    status = Column(String(50), default="pending")  # pending, confirmed, shipped, delivered, cancelled
    
    # Shipping information
    shipping_name = Column(String(100), nullable=False)
    shipping_email = Column(String(100), nullable=False)
    shipping_phone = Column(String(20))
    shipping_address = Column(Text, nullable=False)
    shipping_city = Column(String(100), nullable=False)
    shipping_state = Column(String(100))
    shipping_postal_code = Column(String(20), nullable=False)
    shipping_country = Column(String(100), nullable=False)
    
    # Payment information
    payment_method = Column(String(50))  # stripe, paypal, etc.
    payment_status = Column(String(50), default="pending")
    payment_id = Column(String(200))  # External payment ID
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

# Database functions
def get_db_session() -> Generator[Session, None, None]:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Initialize database with tables and sample data"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        app_logger.info("Database tables created successfully")
        
        # Add sample data
        db = SessionLocal()
        try:
            # Check if data already exists
            if db.query(Category).count() == 0:
                create_sample_data(db)
                app_logger.info("Sample data created successfully")
            else:
                app_logger.info("Sample data already exists")
        finally:
            db.close()
            
    except Exception as e:
        app_logger.error(f"Error initializing database: {e}")
        raise

def create_sample_data(db: Session):
    """Create sample categories and products"""
    
    # Categories
    categories = [
        Category(
            name="Prospex",
            description="Professional sports watches built for adventure and precision",
            image_url="https://source.unsplash.com/400x300/?seiko+prospex+sport+watch"
        ),
        Category(
            name="Presage",
            description="Elegant dress watches showcasing Japanese craftsmanship",
            image_url="https://source.unsplash.com/400x300/?seiko+presage+dress+watch"
        ),
        Category(
            name="Astron",
            description="Solar GPS watches representing cutting-edge technology",
            image_url="https://source.unsplash.com/400x300/?seiko+astron+solar+watch"
        ),
        Category(
            name="5 Sports",
            description="Automatic sports watches with modern style and reliability",
            image_url="https://source.unsplash.com/400x300/?seiko+5+sports+automatic"
        )
    ]
    
    for category in categories:
        db.add(category)
    db.commit()
    
    # Products
    products = [
        # Prospex Collection
        Product(
            name="Seiko Prospex Solar Diver",
            model_number="SNE497",
            description="Professional solar-powered dive watch with 200m water resistance. Features unidirectional rotating bezel and luminous hands for underwater visibility.",
            price=295.00,
            original_price=350.00,
            stock_quantity=15,
            category_id=1,
            movement_type="Solar Quartz",
            case_material="Stainless Steel",
            case_diameter="43.5mm",
            water_resistance="200m",
            strap_material="Silicone",
            main_image_url="https://source.unsplash.com/600x600/?seiko+prospex+diver+watch",
            detail_image_url="https://source.unsplash.com/600x600/?watch+mechanism+detail",
            lifestyle_image_url="https://source.unsplash.com/600x600/?diving+watch+lifestyle",
            is_featured=True,
            is_on_sale=True
        ),
        Product(
            name="Seiko Prospex Automatic GMT",
            model_number="SSK001",
            description="Robust GMT watch perfect for world travelers. Features 24-hour GMT hand and date display with automatic movement.",
            price=425.00,
            stock_quantity=8,
            category_id=1,
            movement_type="Automatic",
            case_material="Stainless Steel",
            case_diameter="42mm",
            water_resistance="100m",
            strap_material="Stainless Steel",
            main_image_url="https://source.unsplash.com/600x600/?seiko+gmt+automatic+watch",
            detail_image_url="https://source.unsplash.com/600x600/?gmt+watch+face+detail",
            lifestyle_image_url="https://source.unsplash.com/600x600/?travel+watch+lifestyle",
            is_featured=True
        ),
        
        # Presage Collection
        Product(
            name="Seiko Presage Cocktail Time",
            model_number="SRPB41",
            description="Elegant automatic dress watch inspired by Japanese cocktail culture. Features power reserve indicator and exhibition case back.",
            price=350.00,
            stock_quantity=12,
            category_id=2,
            movement_type="Automatic",
            case_material="Stainless Steel",
            case_diameter="40.5mm",
            water_resistance="50m",
            strap_material="Leather",
            main_image_url="https://source.unsplash.com/600x600/?seiko+presage+cocktail+dress+watch",
            detail_image_url="https://source.unsplash.com/600x600/?automatic+movement+exhibition",
            lifestyle_image_url="https://source.unsplash.com/600x600/?elegant+dress+watch+lifestyle",
            is_featured=True
        ),
        Product(
            name="Seiko Presage Sharp Edged GMT",
            model_number="SPB221",
            description="Modern interpretation of classic design with GMT functionality. Sharp-edged case design with dual-time capability.",
            price=495.00,
            stock_quantity=6,
            category_id=2,
            movement_type="Automatic",
            case_material="Stainless Steel",
            case_diameter="40.5mm",
            water_resistance="100m",
            strap_material="Stainless Steel",
            main_image_url="https://source.unsplash.com/600x600/?seiko+presage+sharp+edge+gmt",
            detail_image_url="https://source.unsplash.com/600x600/?sharp+edge+watch+design",
            lifestyle_image_url="https://source.unsplash.com/600x600/?business+professional+watch"
        ),
        
        # Astron Collection
        Product(
            name="Seiko Astron GPS Solar",
            model_number="SSE167",
            description="Revolutionary GPS solar watch that adjusts to any timezone automatically. Perpetual calendar and world time functionality.",
            price=1200.00,
            original_price=1400.00,
            stock_quantity=4,
            category_id=3,
            movement_type="GPS Solar",
            case_material="Titanium",
            case_diameter="44.6mm",
            water_resistance="100m",
            strap_material="Titanium",
            main_image_url="https://source.unsplash.com/600x600/?seiko+astron+gps+solar+titanium",
            detail_image_url="https://source.unsplash.com/600x600/?gps+solar+watch+technology",
            lifestyle_image_url="https://source.unsplash.com/600x600/?luxury+technology+watch+lifestyle",
            is_featured=True,
            is_on_sale=True
        ),
        
        # 5 Sports Collection
        Product(
            name="Seiko 5 Sports Automatic",
            model_number="SRPD55",
            description="Classic automatic sports watch with day-date display. Reliable 4R36 movement with 41-hour power reserve.",
            price=195.00,
            stock_quantity=20,
            category_id=4,
            movement_type="Automatic",
            case_material="Stainless Steel",
            case_diameter="42.5mm",
            water_resistance="100m",
            strap_material="Nylon NATO",
            main_image_url="https://source.unsplash.com/600x600/?seiko+5+sports+automatic+nato",
            detail_image_url="https://source.unsplash.com/600x600/?automatic+watch+movement+4r36",
            lifestyle_image_url="https://source.unsplash.com/600x600/?casual+sports+watch+lifestyle"
        ),
        Product(
            name="Seiko 5 Sports Street Style",
            model_number="SRPD79",
            description="Modern street-style automatic watch with bold design. Perfect for everyday wear with reliable automatic movement.",
            price=225.00,
            stock_quantity=18,
            category_id=4,
            movement_type="Automatic",
            case_material="Stainless Steel",
            case_diameter="42.5mm",
            water_resistance="100m",
            strap_material="Silicone",
            main_image_url="https://source.unsplash.com/600x600/?seiko+5+sports+street+style",
            detail_image_url="https://source.unsplash.com/600x600/?modern+watch+design+detail",
            lifestyle_image_url="https://source.unsplash.com/600x600/?street+style+watch+casual"
        )
    ]
    
    for product in products:
        db.add(product)
    
    # Create admin user
    from app.services.auth_service import AuthService
    auth_service = AuthService()
    
    admin_user = User(
        username="admin",
        email="admin@seikostore.com",
        full_name="Store Administrator",
        hashed_password=auth_service.get_password_hash("admin123"),
        is_admin=True
    )
    db.add(admin_user)
    
    # Create demo user
    demo_user = User(
        username="demo",
        email="demo@example.com",
        full_name="Demo User",
        hashed_password=auth_service.get_password_hash("demo123")
    )
    db.add(demo_user)
    
    db.commit()
    app_logger.info("Sample data created: 4 categories, 7 products, 2 users")