package com.example.demo.repository;
import com.example.demo.model.Product;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicLong;

@Repository

public class ProductRepository {
    // public private y protected
    private final List<Product>products= new ArrayList<>();
    private final AtomicLong counterId = new AtomicLong(1);

    public List<Product> getProducts(){
        return products;
    }


    public Optional<Product> getProductById(Long id){
        return  products.stream().filter(
                (Product product)-> product.id().equals(id)
        ).findFirst();
    }

    public Product saveProduct(String name, double price) {
        Product productNew = new Product(counterId.getAndIncrement(), name, price);
        products.add(productNew);
        return productNew;
    }
}
