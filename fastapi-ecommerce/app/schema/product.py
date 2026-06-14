from pydantic import BaseModel,Field
from typing import Annotated,Literal
from uuid import UUID

class Product(BaseModel):
    id: UUID
    sku: Annotated[str, Field(
        min_length=6,
        max_length=30,
        title="SKU",
        description="Stock Keeping Unit, unique identifier for the product",
        examples=["SKU12345", "PROD-001", "ITEM-2024"]
        )
    ]
    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=80,
            title="Product Name",
            description="Name of the product",
            examples=["Xiomi Redmi Note 12 Pro", "Apple iPhone 14 Pro Max"],
        ),
    ]
    description: Annotated[
        str,
        Field(max_length=200,description="Short description of the product"),
    ]
    category: Annotated[
        str,
        Field(
            min_length = 3,
            max_length=30,
            description="Category of the product",
            examples=["Smartphones", "Laptops", "Headphones"],
        )
    ]
    brand: Annotated[
        str,
        Field(min_length=2, max_length=50,  examples=["Apple", "Samsung", "Sony"]),
    ]

    price: Annotated[
        float,Field(gt=0,strict = True ,description="Price of the product in INR")
    ]

    currency: Literal["INR"] = "INR"

    discount_percent: Annotated[
        int,
        Field(
            ge=0,
            le=90,
            description="Discount percentage on the product (0-90)",
        ),
    ]

    stock: Annotated[
        int,
        Field(
            ge=0,
            description="Available stock quantity for the product",
        ),
    ]

    is_active: Annotated[
        bool,
        Field(description="Indicates if the product is active and available for purchase"),
    ]

    rating: Annotated[
        float,
        Field(
            ge=0,
            le=5,
            strict = True,
            description="Average customer rating for the product (0-5)",
        ),
    ]
    
    tags: Annotated[
        Optional[list[str]], Field(
            default=None,
            max_length=10,
            description="List of tags associated with the product (max 10 tags)",
        )
    ]

    image_url: Annotated[
        list[AnyUrl], Field(
            max_length=1,
            description="List of image URLs for the product",
        )
    ]    