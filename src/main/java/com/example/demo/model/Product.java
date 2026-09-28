package com.example.demo.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Table;

@Entity
@Table(name = "products")

public class Product(Long id,String nombre ,double precio) {

    @Id
    @Size(max = 100)
    @Column(nullable = false, length = 100)
    @GeneratedValue(strategy = GenerationType.IDENTITY) // Generar el ID de forma automatica
    private Long id;


    @NotBlank
    @Size(max = 120)
    @Column(nullable = false, length = 120)
    private String name;

    @NotNull
    @Positive
    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal price;

    public Product(String name, BigDecimal price) {
        this.name = name;
        this.price = price;
    }

}
