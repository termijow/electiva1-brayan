package com.example.demo.controller;

import com.example.demo.model.Product;
import com.example.demo.service.ProductService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class ProductController {
    private final ProductService productService;

    // TODO: revisar como crear los constructores de manera automatica (por ejemplo con Lombok @RequiredArgsConstructor).
    public ProductController(ProductService productService) {
        this.productService = productService;
    }

    @GetMapping({"/", "/products"})
    public List<Product> getAll() {
        return productService.getProducts();
    }

    @GetMapping("/products/{id}")
    public ResponseEntity<Product> getById(@PathVariable Long id) {
        return productService.getProductById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping({"/", "/products"}) 
    public Product create(@RequestParam String name, @RequestParam double price) {
        return productService.createProduct(name, price);
    }
}
