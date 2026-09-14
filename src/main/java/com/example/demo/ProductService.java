package com.example.demo;

import org.apache.tomcat.util.http.fileupload.MultipartStream;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import com.example.demo.model.Product;
import com.example.demo.repository.ProductRepository;
import org.springframework.stereotype.Service;

@SpringBootApplication
public class ProductService {
	private ProductRepository productRepository;

	// investigar como podemos mejorar esto "automatizarlo"
	public ProductService(ProductRepository productRepository) {
		this.productRepository = productRepository;
	}

	public List<Product> getProducts () {
		return this.productRepository.getProducts();
	}

	public Product createProduct(String name, double price) {
		if(name == null || name.isBlank()) {
			throw new IllegalArgumentException("El nombre es requerido");
		}
		if (price <= 0) {
			throw new IllegalArgumentException("El precio no puede ser un valor negativo");
		}
		return this.productRepository.saveProduct(name, price);
	}
}
