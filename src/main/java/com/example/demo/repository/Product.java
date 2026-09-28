// package com.electiva.api.model;

// public record Product(
//         Long id,
//         String name,
//         Double price) 
        
//         {

//         }
import com.example.demo.model.Product;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProductRepository extends JpaRepository<Product, Long> {

    boolean existsByNameIgnoreCase(String name);
    List<Product> findByNameContainingIgnoreCase(String name);

    
}