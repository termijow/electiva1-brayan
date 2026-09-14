package com.example.demo.service;

import com.example.demo.model.Product;
import com.example.demo.repository.ProductRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class ProductService {
	private final ProductRepository productRepository;

	// Investigar como podemos mejorar esto "automatizarlo" (por ejemplo con Lombok @RequiredArgsConstructor)
	public ProductService(ProductRepository productRepository) {
		this.productRepository = productRepository;
	}

	public List<Product> getProducts() {
		return this.productRepository.getProducts();
	}

	public Optional<Product> getProductById(Long id) {
		return this.productRepository.getProductById(id);
	}

	public Product createProduct(String name, double price) {
		if (name == null || name.isBlank()) {
			throw new IllegalArgumentException("El nombre es requerido");
		}
		if (price <= 0) {
			throw new IllegalArgumentException("El precio no puede ser un valor negativo");
		}
		return this.productRepository.saveProduct(name, price);
	}
}
