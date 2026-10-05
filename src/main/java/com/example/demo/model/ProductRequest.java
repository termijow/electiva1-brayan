package com.example.demo.model;

package jakarta.validation.constraints.NotBlank;
package jakarta.validation.constraints.Size;

public record ProductRequest(
    @NotBlank(message = "El nombre es requerido")
    @Size(max = 100, message = "El nombre no puede superar la cantidad de 100 caracteres")
    String name,

    @NotNull
    @Positive
    @Digits(integer = 10, fraction = 2)
    BigDecimal price
) 

{
    public ProductRequest {
        if(name != null) {
            name = name.trim();
        }
    }
}