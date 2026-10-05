package com.example.demo.service;

import com.example.demo.model.Product;
import com.example.demo.model.ProductResponse;
import com.example.demo.repository.ProductRepository;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

@Service
public class ProductService {
    private final ProductRepository productRepository;

    public ProductService(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    public List<ProductResponse> getProducts() {
        return this.productRepository.findAll().stream()
                .map(ProductResponse::from)
                .toList();
    }

    public Optional<ProductResponse> getProductById(Long id) {
        return this.productRepository.findById(id)
                .map(ProductResponse::from);
    }

    public ProductResponse createProduct(String name, BigDecimal price) {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("El nombre es requerido");
        }
        if (price == null || price.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("El precio no puede ser un valor negativo o cero");
        }

        Product productSave = this.productRepository.save(new Product(name, price));
        return ProductResponse.from(productSave);
    }
}
