from pydantic import BaseModel,Field,field_validator,model_validator,computed_field,EmailStr,AnyUrl
from typing import Annotated,Literal,Optional
from uuid import UUID
from datetime import datetime


class Seller(BaseModel):
    id: UUID
    name: Annotated[
        str,
        Field(
            min_length=2,
            max_length=60,
            title="Seller Name",
            description="Name of the Seller",
            examples=["Samsung Store", "Apple Store India"],
        ),
    ]
    email: EmailStr
    website: AnyUrl

    @field_validator("email",mode="after")
    @classmethod
    def validate_seller_email_domain(cls,value: EmailStr):
        allowed_domains = ["mistore.in","hpworld.in"]

        domain = str(value).split("@")[-1].lower()
        if domain not in allowed_domains:
            raise ValueError(f"Email domain {domain} is not allowed")
        return value

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
    
    seller: Seller
    created_at: datetime

    @field_validator("sku",mode="after")
    @classmethod
    def validate_sku_format(cls,value: str):
        if "-" not in value:
            raise ValueError("SKU mut have '-")
        last = value.split('-')[-1]
        if not (len(last) == 3 and last.isdigit()):
            raise ValueError("SKU must end with a 3 digit sequence like -234")
        return value
    
    @model_validator(mode="after")
    @classmethod
    def validate_business_rules(cls,model:"Product"):
        if model.stock == 0 and model.is_active is True:
            raise ValueError("If stackl is 0, is_active must be false")
        if model.discount_percent > 0 and model.rating == 0:
            raise ValueError("Discounted Price must have the rating (rating != 0)")
        
        return model

    @computed_field
    @property
    def final_price(self) -> float:
        return round(self.price * (1-self.discount_percent/100),2)
    

        
