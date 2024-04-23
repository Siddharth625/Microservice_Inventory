from fastapi import FastAPI
import uvicorn
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:3000'],
    allow_methods = ['*'],
    allow_headers = ['*']
)

redis = get_redis_connection(
    host="redis-14215.c15.us-east-1-4.ec2.cloud.redislabs.com",
    port=14215,
    password = "vss9C1FaqVYmZAVeUUfFlqy3vFJENvZO",
    decode_responses = True
)

class Product(HashModel):
    name: str
    price: float
    quantity_available: int

    class Meta:
        database = redis

def format(pk: str):
    product = Product.get(pk)
    return {
        "id" : product.pk,
        "name" : product.name,
        "price" : product.price,
        "quantity" : product.quantity_available
    }

# GET APIs - Products
@app.get('/products')
def Allproducts():
    return[format(pk) for pk in Product.all_pks()]

@app.get('/products/{id}', response_model=Product)
def  Getproduct(id :str):
    return Product.get(pk=id)

# POST APIs - Products
@app.post('/products')
def createProducts(product: Product):
    return product.save()

# DELETE APIs - Products
@app.delete('/product/{id}')
def deleteProduct(id :str):
    return Product.delete(pk=id)


if __name__ == "__main__":
    uvicorn.run("main:app")