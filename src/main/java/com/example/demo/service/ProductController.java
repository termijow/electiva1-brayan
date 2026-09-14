package com.example.demo.service;

import com.example.demo.ProductService;
import com.example.demo.model.Product;
import com.example.demo.repository.ProductRepository;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.rmi.server.ServerCloneException;
import java.util.List;

@RestController
public class ProductController {
    private ProductService productService;

    //TODO: revisar como crear los constructores de manera automatica.
    public ProductController(ProductService productService) {
        this.productService = productService;
    }

    @GetMapping("/")
    public List<Product> getAll() {
        return productService.getProducts();
    }

    @PostMapping("/")
    public Product create(@RequestParam String name, @RequestParam double price) {
        return productService.createProduct(name, price);
    }
}
